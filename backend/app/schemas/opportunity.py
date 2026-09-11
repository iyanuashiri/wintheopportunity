from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.opportunity import Category


class OpportunityCreate(BaseModel):
    """Payload for creating/upserting an opportunity via the API."""

    title: str
    organization_name: str
    organization_url: str
    opportunity_url: str
    source_url: str | None = None
    application_url: str | None = None
    description: str | None = None
    eligibility_criteria: str | None = None
    category: Category = Category.GRANT
    start_date: datetime | None = None
    deadline: datetime | None = None
    scrapped_webpage: str | None = None


class OpportunityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    organization_name: str
    organization_url: str
    opportunity_url: str
    source_url: str | None
    application_url: str | None
    description: str | None
    eligibility_criteria: str | None
    category: Category
    start_date: datetime | None
    deadline: datetime | None
    scrapped_webpage: str | None
    created_at: datetime


class OpportunityUpsertResult(BaseModel):
    """Response for a bulk upsert of opportunities."""

    created: int
    updated: int
    opportunities: list[OpportunityRead]