from datetime import datetime, timezone
from sqlalchemy import (
    ForeignKey, String, Text, DateTime, Float, Integer, Enum, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.core.database import Base


class Category(str, enum.Enum):
    GRANT = "grant"
    SCHOLARSHIP = "scholarship"
    FELLOWSHIP = "fellowship"
    ACCELERATOR = "accelerator"
    AWARD = "award"
    CONTEST = "contest"
    TRAINING = "training"
    OTHER = "other"


class Opportunity(Base):
    __tablename__ = "opportunities"
    __table_args__ = (
        # An opportunity is uniquely identified by its landing page URL
        # combined with its start date and deadline. The same URL can be
        # reused yearly (the page content changes), so URL alone is not unique.
        UniqueConstraint(
            "opportunity_url", "start_date", "deadline",
            name="uq_opportunity_url_start_deadline",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    organization_name: Mapped[str] = mapped_column(String(255))
    organization_url: Mapped[str] = mapped_column(String(500))
    opportunity_url: Mapped[str] = mapped_column(String(500))
    source_url: Mapped[str | None] = mapped_column(String(255))
    application_url: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    eligibility_criteria: Mapped[str | None] = mapped_column(Text)
    category: Mapped[Category] = mapped_column(Enum(Category), default=Category.GRANT)
    start_date: Mapped[datetime.datetime | None] = mapped_column(DateTime)
    deadline: Mapped[datetime.datetime | None] = mapped_column(DateTime)
    
    scrapped_webpage: Mapped[str | None] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


class RecommendationStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    DISMISSED = "dismissed"


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"))
    relevance_score: Mapped[float] = mapped_column(Float)
    match_reason: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(50), default="hybrid")
    status: Mapped[RecommendationStatus] = mapped_column(
        Enum(RecommendationStatus), default=RecommendationStatus.ACTIVE
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
