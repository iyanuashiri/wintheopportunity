"""Structured output models for the opportunity scraping agent.

The ``Category`` enum is defined here (rather than imported from the
backend) so this service is fully standalone and does not depend on the
backend's database models.
"""

import enum

from pydantic import BaseModel, Field


class Category(str, enum.Enum):
    GRANT = "grant"
    SCHOLARSHIP = "scholarship"
    FELLOWSHIP = "fellowship"
    ACCELERATOR = "accelerator"
    AWARD = "award"
    CONTEST = "contest"
    TRAINING = "training"
    OTHER = "other"


class ScrapedOpportunity(BaseModel):
    """A single opportunity discovered on a listing page."""

    title: str = Field(description="Title of the opportunity")
    organization_name: str = Field(description="Name of the organization offering it")
    organization_url: str = Field(description="URL of the organization's website")
    opportunity_url: str = Field(description="URL of the specific opportunity page")
    source_url: str | None = Field(
        default=None, description="URL where this opportunity was scraped"
    )
    application_url: str | None = Field(
        default=None, description="Direct URL where applications are submitted"
    )
    description: str | None = Field(default=None, description="Short description")
    eligibility_criteria: str | None = Field(
        default=None, description="Who is eligible to apply"
    )
    category: Category = Field(default=Category.GRANT, description="Opportunity category")
    start_date: str | None = Field(
        default=None, description="Start date as ISO date string, if known"
    )
    deadline: str | None = Field(
        default=None, description="Application deadline as ISO date string, if known"
    )
    scrapped_webpage: str | None = Field(
        default=None, description="Raw HTML of the detail page, for reference"
    )


class ScrapeResult(BaseModel):
    """Result of scraping a listing page."""

    opportunities: list[ScrapedOpportunity] = Field(
        default_factory=list, description="Opportunities found on the page"
    )
    next_urls: list[str] = Field(
        default_factory=list, description="Additional listing URLs to visit"
    )