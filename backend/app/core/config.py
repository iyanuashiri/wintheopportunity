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

    # Base URL of this API, used by agents to call endpoints over HTTP
    api_base_url: str = Field(default="http://localhost:8000", alias="API_BASE_URL")

    # Agent / LLM configuration
    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1", alias="OPENROUTER_BASE_URL"
    )
    agent_model_id: str = Field(
        default="deepseek/deepseek-v4-flash-0731", alias="AGENT_MODEL_ID"
    )


settings = Settings()