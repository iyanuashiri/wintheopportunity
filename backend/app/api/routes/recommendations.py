from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep, CurrentUserDep
from app.crud import recommendation as crud_recommendation
from app.models.opportunity import Recommendation
from app.schemas.recommendation import (
    RecommendationCreate,
    RecommendationCreateResult,
    RecommendationRead,
)

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RecommendationCreateResult)
async def create_recommendations(
    recommendations: list[RecommendationCreate],
    session: SessionDep,
) -> RecommendationCreateResult:
    """Bulk create recommendations. Used by the recommender agent."""
    saved: list[Recommendation] = []
    for rec in recommendations:
        saved.append(crud_recommendation.create_recommendation(session, rec))
    return RecommendationCreateResult(created=len(saved), recommendations=saved)


@router.get("/", response_model=list[RecommendationRead])
async def list_my_recommendations(
    session: SessionDep,
    current_user: CurrentUserDep,
    skip: int = 0,
    limit: int = 50,
) -> list[RecommendationRead]:
    """List the current user's active recommendations."""
    return crud_recommendation.get_recommendations_for_user(
        session, current_user.id, skip=skip, limit=limit
    )


@router.get("/opportunity-ids/", response_model=list[int])
async def get_recommended_opportunity_ids(
    session: SessionDep,
    current_user: CurrentUserDep,
) -> list[int]:
    """Get the opportunity IDs already recommended to the current user.

    Used by the recommender agent to avoid re-recommending opportunities.
    """
    return sorted(
        crud_recommendation.get_recommended_opportunity_ids(session, current_user.id)
    )