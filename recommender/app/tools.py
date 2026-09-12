"""Tools for the recommender agent.

These tools interact with the backend API over HTTP:
- fetch_new_opportunities: get opportunities created in the lookback window.
- fetch_ngos: get all NGO profiles.
- save_recommendations: persist scored recommendations to the backend.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

import httpx
from strands import tool

from app.config import settings

logger = logging.getLogger(__name__)


@tool
def fetch_new_opportunities() -> list[dict]:
    """Fetch opportunities created in the recent lookback window.

    Returns:
        list[dict]: List of opportunity dicts from the backend API.
    """
    since = datetime.now(timezone.utc) - timedelta(hours=settings.lookback_hours)
    resp = httpx.get(
        f"{settings.api_base_url}/api/v1/opportunities/",
        params={"skip": 0, "limit": 500},
        timeout=60,
    )
    resp.raise_for_status()
    opportunities = resp.json()
    # Filter to those created within the lookback window
    recent = []
    for opp in opportunities:
        created = opp.get("created_at")
        if created:
            try:
                created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                # The backend may return naive datetimes; assume UTC if so.
                if created_dt.tzinfo is None:
                    created_dt = created_dt.replace(tzinfo=timezone.utc)
                if created_dt >= since:
                    recent.append(opp)
            except ValueError:
                recent.append(opp)
        else:
            recent.append(opp)
    return recent


@tool
def fetch_ngos() -> list[dict]:
    """Fetch all NGO profiles from the backend.

    Returns:
        list[dict]: List of NGO profile dicts.
    """
    resp = httpx.get(
        f"{settings.api_base_url}/api/v1/organizations/",
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


@tool
def fetch_recommended_opportunity_ids(user_id: int) -> list[int]:
    """Fetch the opportunity IDs already recommended to a user.

    Args:
        user_id (int): The NGO user's ID.

    Returns:
        list[int]: Opportunity IDs already recommended to this user.
    """
    resp = httpx.get(
        f"{settings.api_base_url}/api/v1/recommendations/opportunity-ids/",
        params={"user_id": user_id},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


@tool
def fetch_all_opportunities() -> list[dict]:
    """Fetch all opportunities from the backend (for new-user onboarding).

    Returns:
        list[dict]: List of opportunity dicts from the backend API.
    """
    resp = httpx.get(
        f"{settings.api_base_url}/api/v1/opportunities/",
        params={"skip": 0, "limit": 1000},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


@tool
def save_recommendations(
    recommendations: list[dict],
) -> str:
    """Persist scored recommendations to the backend.

    Args:
        recommendations (list[dict]): List of recommendation dicts with
            user_id, opportunity_id, relevance_score, match_reason, source.

    Returns:
        str: Summary of how many recommendations were saved.
    """
    resp = httpx.post(
        f"{settings.api_base_url}/api/v1/recommendations/",
        json=recommendations,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return f"Saved {data.get('created', len(recommendations))} recommendations."


ALL_TOOLS = [
    fetch_new_opportunities,
    fetch_all_opportunities,
    fetch_ngos,
    fetch_recommended_opportunity_ids,
    save_recommendations,
]