"""Configuration for the standalone scraper service.

This is a separate settings class from the backend's ``app.core.config``
because the scraper is deployed as its own service. It only needs the
settings relevant to scraping and calling the backend API.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        populate_by_name=True,
        env_file=".env",
        extra="ignore",
    )

    # Base URL of the backend API this scraper feeds
    api_base_url: str = Field(default="http://localhost:8000", alias="API_BASE_URL")

    # Agent / LLM configuration
    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1", alias="OPENROUTER_BASE_URL"
    )
    agent_model_id: str = Field(
        default="deepseek/deepseek-v4-flash-0731", alias="AGENT_MODEL_ID"
    )

    # Scraper behavior
    max_pages: int = Field(default=3, alias="SCRAPER_MAX_PAGES")


settings = Settings()