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


settings = Settings()