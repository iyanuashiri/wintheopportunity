from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.opportunity import RecommendationStatus


class RecommendationCreate(BaseModel):
    """Payload for creating a recommendation (used by the recommender agent)."""

    user_id: int
    opportunity_id: int
    relevance_score: float
    match_reason: str | None = None
    source: str | None = "hybrid"


class RecommendationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    opportunity_id: int
    relevance_score: float
    match_reason: str | None
    source: str | None
    status: RecommendationStatus
    is_active: bool
    created_at: datetime


class RecommendationCreateResult(BaseModel):
    """Response for a bulk create of recommendations."""

    created: int
    recommendations: list[RecommendationRead]