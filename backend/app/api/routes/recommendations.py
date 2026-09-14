from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep, CurrentUserDep, ServiceOrUserDep
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


@router.get("/all/", response_model=list[RecommendationRead])
async def list_all_recommendations(
    session: SessionDep,
    current_user: ServiceOrUserDep,
    skip: int = 0,
    limit: int = 500,
) -> list[RecommendationRead]:
    """List all active recommendations across all users.

    Service-only endpoint used by the application-scraper agent to process
    every recommendation. Requires a valid service API key.
    """
    if current_user is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only available to services",
        )
    return crud_recommendation.get_all_recommendations(session, skip=skip, limit=limit)


@router.get("/opportunity-ids/", response_model=list[int])
async def get_recommended_opportunity_ids(
    session: SessionDep,
    current_user: ServiceOrUserDep,
    user_id: int | None = None,
) -> list[int]:
    """Get the opportunity IDs already recommended to a user.

    Accepts either a user JWT (uses the authenticated user) or a service
    API key (uses the ``user_id`` query param). Used by the recommender
    agent to avoid re-recommending opportunities.
    """
    target_user_id = current_user.id if current_user else user_id
    if target_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id is required when authenticating as a service",
        )
    return sorted(
        crud_recommendation.get_recommended_opportunity_ids(session, target_user_id)
    )