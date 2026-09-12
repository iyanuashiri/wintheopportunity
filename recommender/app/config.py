"""Configuration for the standalone recommender service.

This service runs daily to match new opportunities against NGO profiles
and produce personalized recommendations. It is deployed separately from
the backend and calls the backend API over HTTP.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        populate_by_name=True,
        env_file=".env",
        extra="ignore",
    )

    # Base URL of the backend API this service reads from / writes to
    api_base_url: str = Field(default="http://localhost:8000", alias="API_BASE_URL")

    # Agent / LLM configuration (Gemma 4 31B via OpenRouter for scoring)
    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1", alias="OPENROUTER_BASE_URL"
    )
    agent_model_id: str = Field(
        default="google/gemma-4-31b-it", alias="AGENT_MODEL_ID"
    )

    # RAG / vector store configuration
    chroma_path: str = Field(default="./chroma_db", alias="CHROMA_PATH")
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2", alias="EMBEDDING_MODEL"
    )
    top_k: int = Field(default=10, alias="RECOMMENDER_TOP_K")

    # How far back to look for "new" opportunities (hours)
    lookback_hours: int = Field(default=24, alias="RECOMMENDER_LOOKBACK_HOURS")


settings = Settings()