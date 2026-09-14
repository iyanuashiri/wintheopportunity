"""Onboarding route: triggers the agent pipeline for a new user.

When a new NGO completes their profile, this endpoint generates their first
recommendations and applications.

DEMO MODE: For the demo, this endpoint does fast, deterministic work
(keyword matching + reusing real extracted questions) instead of running the
slow LLM/Playwright agents. The real agents remain available for normal use.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status

from app import crud
from app.api.deps import SessionDep, CurrentUserDep
from app.models.opportunity import Opportunity
from app.models.application import Application
from app.schemas.recommendation import RecommendationCreate
from app.schemas.application import ApplicationCreate, QuestionCreate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


def _score_opportunity(profile_text: str, opp: Opportunity) -> float:
    """Simple keyword-based relevance score for the demo.

    Counts how many profile keywords appear in the opportunity's title,
    description, and eligibility. Returns a score in [0, 1].
    """
    keywords = [
        w.strip().lower()
        for w in profile_text.replace(",", " ").split()
        if len(w.strip()) > 2
    ]
    if not keywords:
        return 0.0

    haystack = " ".join(
        filter(
            None,
            [
                opp.title or "",
                opp.description or "",
                opp.eligibility_criteria or "",
                opp.organization_name or "",
            ],
        )
    ).lower()

    hits = sum(1 for kw in keywords if kw in haystack)
    # Normalize: a few strong hits should reach a high score
    return min(1.0, hits / max(3, len(keywords)) * 1.5)


def _match_reason(opp: Opportunity) -> str:
    """Generate a plausible match reason for the demo."""
    return (
        f"Strong alignment with your organization's focus areas and mission. "
        f"{opp.organization_name} is offering this {opp.category.value} opportunity "
        f"which matches your profile."
    )


def _demo_questions() -> list[QuestionCreate]:
    """Return realistic application questions for the demo.

    Uses the real questions already extracted from the AU-EU Youth Action Lab
    form (stored in the DB) as a template.
    """
    return [
        QuestionCreate(
            question_text="Organization name",
            field_type="text",
            is_required=True,
            order_index=0,
        ),
        QuestionCreate(
            question_text="Country of registration",
            field_type="text",
            is_required=True,
            order_index=1,
        ),
        QuestionCreate(
            question_text="Contact email",
            field_type="text",
            is_required=True,
            order_index=2,
        ),
        QuestionCreate(
            question_text="Describe your proposed project and how it addresses a global challenge",
            field_type="textarea",
            is_required=True,
            order_index=3,
        ),
        QuestionCreate(
            question_text="Which SDG / Agenda 2063 goal does your innovation address?",
            field_type="dropdown",
            is_required=True,
            order_index=4,
        ),
        QuestionCreate(
            question_text="What is your estimated budget for this project?",
            field_type="text",
            is_required=False,
            order_index=5,
        ),
    ]


@router.post("/recommend/", status_code=status.HTTP_200_OK)
async def trigger_onboarding(
    session: SessionDep,
    current_user: CurrentUserDep,
) -> dict:
    """Generate first recommendations + applications for the current user.

    DEMO MODE: fast, deterministic keyword matching + reusable questions.
    Does NOT run the slow LLM/Playwright agents.

    Returns:
        dict: Summary of what was generated.
    """
    user_id = current_user.id

    # 1. Load the user's organization profile
    org = crud.get_organization_by_user(session, user_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please complete your organization profile first.",
        )
    profile_text = " ".join(
        filter(
            None,
            [
                org.org_name or "",
                org.mission_statement or "",
                org.focus_areas or "",
                org.target_beneficiaries or "",
                org.background_info or "",
            ],
        )
    )

    # 2. Fetch all opportunities and score them against the profile
    opportunities = crud.get_all_opportunities(session, skip=0, limit=100)
    scored = []
    for opp in opportunities:
        score = _score_opportunity(profile_text, opp)
        if score > 0:
            scored.append((score, opp))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:6]

    # 3. Create recommendations (skip ones already recommended)
    existing_ids = crud.get_recommended_opportunity_ids(session, user_id)
    created_recs = 0
    for score, opp in top:
        if opp.id in existing_ids:
            continue
        crud.create_recommendation(
            session,
            RecommendationCreate(
                user_id=user_id,
                opportunity_id=opp.id,
                relevance_score=round(score, 2),
                match_reason=_match_reason(opp),
                source="demo",
            ),
        )
        created_recs += 1

    # 4. Create applications for the top recommendations (reuse real questions)
    created_apps = 0
    for score, opp in top[:3]:
        existing_app = (
            session.query(Application)
            .filter(
                Application.user_id == user_id,
                Application.opportunity_id == opp.id,
            )
            .first()
        )
        if existing_app:
            continue
        crud.create_application(
            session,
            ApplicationCreate(
                title=opp.title,
                user_id=user_id,
                opportunity_id=opp.id,
                application_url=opp.application_url,
                mode="url_scrape",
                questions_extracted=True,
                questions=_demo_questions(),
            ),
            user_id,
        )
        created_apps += 1

    return {
        "status": "complete",
        "user_id": user_id,
        "recommendations_generated": created_recs,
        "applications_extracted": created_apps,
    }