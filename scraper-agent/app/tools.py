"""Tools for the opportunity scraping agent.

All agent tools live here in a dedicated file so the agent orchestration
in ``agent.py`` stays clean and focused on the agent loop.
"""

from __future__ import annotations

import logging
from typing import Annotated

import httpx
from bs4 import BeautifulSoup
from strands import tool

from app.config import settings
from app.scraper import extract_detail_links, scrape_webpage

logger = logging.getLogger(__name__)


def _headers() -> dict[str, str]:
    """Return auth headers for backend calls (service API key if configured)."""
    headers = {}
    if settings.service_api_key:
        headers["X-API-Key"] = settings.service_api_key
    return headers


def _html_to_text(html: str, max_chars: int = 12000) -> str:
    """Strip HTML tags and limit the text length to avoid context overflow."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    return text[:max_chars]


@tool
async def fetch_listing(url: str, is_paginated: bool = False, max_pages: int = 3) -> str:
    """Fetch a listing page (and its paginated pages) using Playwright.

    Args:
        url (str): The URL of the listing page to fetch.
        is_paginated (bool): Whether the page has pagination to walk through.
        max_pages (int): Maximum number of pages to scrape when paginated.

    Returns:
        str: The visible text content of the page(s), HTML stripped.
    """
    documents = await scrape_webpage(url, is_paginated=is_paginated, max_pages=max_pages)
    combined = "\n\n--- PAGE BREAK ---\n\n".join(documents)
    return _html_to_text(combined)


@tool
async def fetch_listing_links(url: str, is_paginated: bool = False, max_pages: int = 3) -> list[str]:
    """Fetch a listing page and return the detail-page URLs it contains.

    Args:
        url (str): The URL of the listing page to fetch.
        is_paginated (bool): Whether the page has pagination to walk through.
        max_pages (int): Maximum number of pages to scrape when paginated.

    Returns:
        list[str]: The detail page URLs found on the listing page(s).
    """
    documents = await scrape_webpage(url, is_paginated=is_paginated, max_pages=max_pages)
    links: set[str] = set()
    for doc in documents:
        links.update(extract_detail_links(doc, url))
    return list(links)


@tool
async def fetch_detail(url: str) -> str:
    """Fetch a single opportunity detail page using Playwright.

    Args:
        url (str): The URL of the detail page to fetch.

    Returns:
        str: The visible text content of the detail page, HTML stripped.
    """
    documents = await scrape_webpage(url, is_paginated=False)
    return _html_to_text(documents[0])


@tool
async def fetch_detail_html(url: str) -> str:
    """Fetch a single opportunity detail page and return its raw HTML.

    Use this to capture the full page content for the ``scrapped_webpage``
    field, so the opportunity can be referenced later without re-fetching.

    Args:
        url (str): The URL of the detail page to fetch.

    Returns:
        str: The raw HTML of the detail page.
    """
    documents = await scrape_webpage(url, is_paginated=False)
    return documents[0]


@tool
def save_opportunities(
    opportunities: Annotated[list[dict], "List of opportunity dicts to persist"],
) -> str:
    """Persist scraped opportunities by calling the backend API (upsert by URL).

    Args:
        opportunities (list[dict]): List of opportunity dictionaries.

    Returns:
        str: Summary of how many opportunities were created vs updated.
    """
    resp = httpx.post(
        f"{settings.api_base_url}/api/v1/opportunities/upsert/",
        json=opportunities,
        headers=_headers(),
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return f"Created {data['created']} opportunities, updated {data['updated']}."


# Convenience list of all tools for the agent
ALL_TOOLS = [
    fetch_listing,
    fetch_listing_links,
    fetch_detail,
    fetch_detail_html,
    save_opportunities,
]