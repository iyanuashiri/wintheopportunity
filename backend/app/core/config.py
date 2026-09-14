from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        populate_by_name=True,
        env_file=".env",
        extra="ignore",
    )

    database_url: str = Field(default="sqlite:///./wintheopportunity.db", alias="DATABASE_URL")
    secret_key: str = Field(default="development-only-change-this-secret", alias="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Service API key used by agent services to authenticate without a user login
    service_api_key: str = Field(default="", alias="SERVICE_API_KEY")

    # Base URL of this API, used by agents to call endpoints over HTTP
    api_base_url: str = Field(default="http://localhost:8000", alias="API_BASE_URL")

    # Absolute paths to the standalone agent service directories (for onboarding triggers)
    recommender_dir: str = Field(
        default="", alias="RECOMMENDER_DIR"
    )
    application_scraper_dir: str = Field(
        default="", alias="APPLICATION_SCRAPER_DIR"
    )

    # Agent / LLM configuration
    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1", alias="OPENROUTER_BASE_URL"
    )
    agent_model_id: str = Field(
        default="deepseek/deepseek-v4-flash-0731", alias="AGENT_MODEL_ID"
    )


settings = Settings()