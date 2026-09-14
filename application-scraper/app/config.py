"""Configuration for the standalone application form scraper agent."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        populate_by_name=True,
        env_file=".env",
        extra="ignore",
    )

    # Base URL of the backend API this service writes to
    api_base_url: str = Field(default="http://localhost:8000", alias="API_BASE_URL")

    # Service API key used to authenticate with the backend
    service_api_key: str = Field(default="", alias="SERVICE_API_KEY")

    # Agent / LLM configuration
    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1", alias="OPENROUTER_BASE_URL"
    )
    agent_model_id: str = Field(
        default="deepseek/deepseek-v4-flash-0731", alias="AGENT_MODEL_ID"
    )


settings = Settings()