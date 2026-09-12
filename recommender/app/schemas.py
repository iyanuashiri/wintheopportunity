"""Structured output models for the recommender agent."""

from pydantic import BaseModel, Field


class OpportunityData(BaseModel):
    """A single opportunity as returned by the backend API."""

    id: int
    title: str
    organization_name: str
    description: str | None = None
    eligibility_criteria: str | None = None
    category: str | None = None
    deadline: str | None = None


class NGOProfile(BaseModel):
    """An NGO profile as returned by the backend API."""

    user_id: int
    org_name: str
    mission_statement: str | None = None
    focus_areas: str | None = None
    target_beneficiaries: str | None = None
    background_info: str | None = None


class ScoredRecommendation(BaseModel):
    """A single scored recommendation produced by the LLM."""

    opportunity_id: int = Field(description="ID of the recommended opportunity")
    relevance_score: float = Field(
        description="Relevance score from 0.0 to 1.0"
    )
    match_reason: str = Field(
        description="Why this opportunity matches the NGO's profile"
    )


class RecommendationResult(BaseModel):
    """Result of scoring recommendations for a single NGO."""

    user_id: int = Field(description="ID of the NGO user")
    recommendations: list[ScoredRecommendation] = Field(
        default_factory=list, description="Scored recommendations for this NGO"
    )