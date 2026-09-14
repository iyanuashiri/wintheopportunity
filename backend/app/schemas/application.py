from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.application import ApplicationMode, ApplicationStatus


# --- Evaluation Schemas ---
class EvaluationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    score: float
    reasoning: str
    suggestions: str | None
    created_at: datetime


# --- Answer Schemas ---
class AnswerCreate(BaseModel):
    answer_text: str


class AnswerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    answer_text: str
    version: int
    is_final: bool
    created_at: datetime
    evaluations: list[EvaluationRead] = []


# --- Question Schemas ---
class QuestionCreate(BaseModel):
    question_text: str
    field_type: str | None = "text"
    is_required: bool = False
    max_characters: int | None = None
    max_words: int | None = None
    order_index: int = 0
    answers: list[AnswerCreate] = []


class QuestionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_text: str
    field_type: str | None
    is_required: bool
    max_characters: int | None
    max_words: int | None
    order_index: int
    answers: list[AnswerRead] = []


# --- Image Schemas ---
class ImageCreate(BaseModel):
    image_path: str


class ImageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    image_path: str
    created_at: datetime


# --- Application Schemas ---
class ApplicationCreate(BaseModel):
    title: str
    user_id: int | None = None
    opportunity_id: int | None = None
    application_url: str | None = None
    mode: ApplicationMode = ApplicationMode.URL_SCRAPE
    status: ApplicationStatus = ApplicationStatus.DRAFT
    questions_extracted: bool = False
    extraction_note: str | None = None
    extraction_reason: str | None = None
    questions: list[QuestionCreate] = []


# Lightweight schema for List view (Commonly Answered Questions Overview)
class ApplicationReadSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    opportunity_id: int | None
    title: str
    application_url: str | None
    mode: ApplicationMode
    status: ApplicationStatus
    questions_extracted: bool
    extraction_note: str | None
    extraction_reason: str | None
    created_at: datetime
    questions_count: int = 0


# Full schema for Detail view
class ApplicationReadDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    opportunity_id: int | None
    title: str
    application_url: str | None
    mode: ApplicationMode
    status: ApplicationStatus
    questions_extracted: bool
    extraction_note: str | None
    extraction_reason: str | None
    created_at: datetime
    questions: list[QuestionRead] = []
    images: list[ImageRead] = []