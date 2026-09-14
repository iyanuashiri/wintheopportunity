"""Structured output models for the application form scraper agent."""

from pydantic import BaseModel, Field


class ExtractedQuestion(BaseModel):
    """A single question/field extracted from an application form."""

    question_text: str = Field(description="The question or field label")
    field_type: str = Field(
        default="text",
        description="Field type: text, textarea, dropdown, checkbox, file, etc.",
    )
    is_required: bool = Field(
        default=False, description="Whether the field is required"
    )
    max_characters: int | None = Field(
        default=None, description="Max characters, if specified"
    )
    max_words: int | None = Field(
        default=None, description="Max words, if specified"
    )
    order_index: int = Field(
        default=0, description="Order of the field in the form"
    )


class ExtractedApplication(BaseModel):
    """An application form with its extracted questions."""

    title: str = Field(description="The page title (from the <title> tag)")
    application_url: str = Field(description="The form URL")
    questions: list[ExtractedQuestion] = Field(
        default_factory=list, description="Extracted questions/fields"
    )
    extraction_reason: str | None = Field(
        default=None,
        description=(
            "A short, user-friendly explanation of why questions could not be "
            "extracted, e.g. 'This form requires you to log in before the "
            "questions are visible.' Leave null if questions were extracted."
        ),
    )