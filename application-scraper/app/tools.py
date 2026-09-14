"""Tools for the application form scraper agent."""

from __future__ import annotations

import logging

import httpx
from strands import tool

from app.config import settings

logger = logging.getLogger(__name__)


@tool
def fetch_recommendations() -> list[dict]:
    """Fetch all recommendations (with user_id and opportunity_id).

    Returns:
        list[dict]: List of recommendation dicts.
    """
    headers = {}
    if settings.service_api_key:
        headers["X-API-Key"] = settings.service_api_key
    resp = httpx.get(
        f"{settings.api_base_url}/api/v1/recommendations/all/",
        headers=headers,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


@tool
def fetch_opportunity(opportunity_id: int) -> dict:
    """Fetch a single opportunity by id.

    Args:
        opportunity_id (int): The opportunity's ID.

    Returns:
        dict: The opportunity dict.
    """
    resp = httpx.get(
        f"{settings.api_base_url}/api/v1/opportunities/{opportunity_id}/",
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


@tool
def save_application(application: dict) -> str:
    """Create an application with its questions via the backend API.

    Args:
        application (dict): The application dict with title, application_url,
            and questions.

    Returns:
        str: Summary of the created application.
    """
    headers = {}
    if settings.service_api_key:
        headers["X-API-Key"] = settings.service_api_key
    resp = httpx.post(
        f"{settings.api_base_url}/api/v1/applications/",
        json=application,
        headers=headers,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return f"Created application {data['id']} with {len(data['questions'])} questions."


ALL_TOOLS = [
    fetch_recommendations,
    fetch_opportunity,
    save_application,
]