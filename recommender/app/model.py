"""Shared model provider configuration for the recommender agent."""

from strands.models.openai import OpenAIModel

from app.config import settings


def get_agent_model() -> OpenAIModel:
    """Build an OpenAIModel pointed at OpenRouter using app settings."""
    return OpenAIModel(
        client_args={
            "api_key": settings.openrouter_api_key,
            "base_url": settings.openrouter_base_url,
        },
        model_id=settings.agent_model_id,
    )