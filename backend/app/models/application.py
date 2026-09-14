from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Text, DateTime, Integer, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.core.database import Base


class ApplicationMode(str, enum.Enum):
    MANUAL = "manual"
    URL_SCRAPE = "url_scrape"
    SCREENSHOT_VISION = "screenshot_vision"


class ApplicationStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    ARCHIVED = "archived"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    opportunity_id: Mapped[int | None] = mapped_column(ForeignKey("opportunities.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    application_url: Mapped[str | None] = mapped_column(String(500))
    mode: Mapped[ApplicationMode] = mapped_column(Enum(ApplicationMode), default=ApplicationMode.URL_SCRAPE)
    status: Mapped[ApplicationStatus] = mapped_column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT)
    questions_extracted: Mapped[bool] = mapped_column(default=False)
    extraction_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    extraction_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    questions: Mapped[list["Question"]] = relationship(back_populates="application", cascade="all, delete-orphan")
    images: Mapped[list["Image"]] = relationship(back_populates="application", cascade="all, delete-orphan")


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"))
    image_path: Mapped[str] = mapped_column(String(500))

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    application: Mapped["Application"] = relationship(back_populates="images")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"))
    question_text: Mapped[str] = mapped_column(Text)
    field_type: Mapped[str | None] = mapped_column(String(50), default="text")
    is_required: Mapped[bool] = mapped_column(default=False)
    max_characters: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_words: Mapped[int | None] = mapped_column(Integer, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    application: Mapped["Application"] = relationship(back_populates="questions")
    answers: Mapped[list["Answer"]] = relationship(back_populates="question", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    answer_text: Mapped[str] = mapped_column(Text)
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_final: Mapped[bool] = mapped_column(default=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    question: Mapped["Question"] = relationship(back_populates="answers")
    evaluations: Mapped[list["Evaluation"]] = relationship(back_populates="answer", cascade="all, delete-orphan")


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id"))
    score: Mapped[float] = mapped_column(Float)  # e.g., 0.0 - 100.0 or 1-10
    reasoning: Mapped[str] = mapped_column(Text)
    suggestions: Mapped[str | None] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    answer: Mapped["Answer"] = relationship(back_populates="evaluations")