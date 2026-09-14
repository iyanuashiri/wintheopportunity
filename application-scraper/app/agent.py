"""Agent 3: Application Form Web Scraper (standalone service).

This agent runs on a daily schedule (after Agent 2). It:
1. Fetches all recommendations (for all users).
2. For each recommendation, gets the opportunity's application_url.
3. If the URL is public, fetches the form HTML and extracts questions.
4. Creates an Application (with questions if extracted, otherwise URL-only).

The application title is taken from the page's <title> tag.
"""

from __future__ import annotations

import logging

from strands import Agent

from app.config import settings
from app.model import get_agent_model
from app.prompts import EXTRACTION_PROMPT
from app.schemas import ExtractedApplication
from app.scraper import fetch_form_html
from app.tools import (
    ALL_TOOLS,
    fetch_opportunity,
    fetch_recommendations,
    save_application,
)

logger = logging.getLogger(__name__)


def build_agent() -> Agent:
    """Build the application form scraper agent."""
    return Agent(
        model=get_agent_model(),
        tools=ALL_TOOLS,
    )


async def extract_application(url: str) -> ExtractedApplication:
    """Extract questions from an application form URL.

    Args:
        url: The URL of the application form.

    Returns:
        ExtractedApplication: The extracted application data.
    """
    html = await fetch_form_html(url)
    agent = build_agent()
    prompt = EXTRACTION_PROMPT.format(html=html[:20000])
    result = await agent.invoke_async(
        prompt, structured_output_model=ExtractedApplication
    )
    extracted = result.structured_output
    extracted.application_url = url
    return extracted


async def run_daily(user_id: int | None = None) -> list[dict]:
    """Run the daily cron flow: process recommendations.

    Args:
        user_id: If provided, only process recommendations for this user
            (used during onboarding). If None, processes all recommendations.

    Returns:
        list[dict]: Summary of created applications.
    """
    recommendations = fetch_recommendations()
    logger.info("Fetched %d recommendations", len(recommendations))

    results = []
    for rec in recommendations:
        opportunity_id = rec.get("opportunity_id")
        rec_user_id = rec.get("user_id")
        if not opportunity_id:
            continue
        # Filter to a single user during onboarding
        if user_id is not None and rec_user_id != user_id:
            continue

        try:
            opportunity = fetch_opportunity(opportunity_id)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to fetch opportunity %s: %s", opportunity_id, exc)
            continue

        application_url = opportunity.get("application_url")
        title = opportunity.get("title", "Application")

        # Try to extract questions if there's a public URL
        questions = []
        questions_extracted = False
        extraction_note = None
        extraction_reason = None
        if not application_url:
            extraction_note = "No application URL available for this opportunity"
            extraction_reason = "This opportunity doesn't have an application link yet."
        else:
            try:
                extracted = await extract_application(application_url)
                questions = [q.model_dump() for q in extracted.questions]
                questions_extracted = bool(questions)
                title = extracted.title or title
                if not questions_extracted:
                    extraction_note = (
                        "Form fetched but no questions could be extracted "
                        "(likely requires authentication or is JS-rendered)"
                    )
                    extraction_reason = extracted.extraction_reason or (
                        "We couldn't find the application questions on this form. "
                        "It may require you to log in first."
                    )
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "Could not extract questions from %s: %s", application_url, exc
                )
                extraction_note = f"Extraction failed: {exc}"
                extraction_reason = (
                    "We couldn't load the application form to see its questions."
                )

        payload = {
            "title": title,
            "user_id": user_id,
            "opportunity_id": opportunity_id,
            "application_url": application_url,
            "mode": "url_scrape",
            "questions_extracted": questions_extracted,
            "extraction_note": extraction_note,
            "extraction_reason": extraction_reason,
            "questions": questions,
        }
        try:
            summary = save_application(payload)
            results.append(
                {
                    "user_id": rec_user_id,
                    "opportunity_id": opportunity_id,
                    "questions_extracted": questions_extracted,
                    "summary": summary,
                }
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to save application: %s", exc)

    return results


if __name__ == "__main__":
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(description="Run the application scraper agent")
    parser.add_argument(
        "--user-id",
        type=int,
        default=None,
        help="Only process recommendations for this user (onboarding). If omitted, processes all.",
    )
    args = parser.parse_args()

    asyncio.run(run_daily(user_id=args.user_id))