from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    org_name: Mapped[str] = mapped_column(String(255), default="")
    website: Mapped[str | None] = mapped_column(String(255), default="")
    mission_statement: Mapped[str | None] = mapped_column(Text, default="")
    focus_areas: Mapped[str | None] = mapped_column(Text, default="")  # JSON or comma-separated string
    target_beneficiaries: Mapped[str | None] = mapped_column(Text, default="")
    background_info: Mapped[str | None] = mapped_column(Text, default="")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )