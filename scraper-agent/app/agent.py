"""Agent 1: Opportunity Scraping / Research Agent (standalone service).

This agent performs large-scale research of opportunities (grants,
scholarships, fellowships, etc.) from the web. It is designed to run on a
daily schedule.

Design notes:
- This is a standalone service, deployed separately from the backend.
- It does NOT import database models, sessions, or CRUD directly.
  Instead, it persists discovered opportunities by calling the backend's
  HTTP API endpoints (see ``save_opportunities`` tool).
- Web fetching is handled by Playwright (see ``scraper.py``), which supports
  pagination so the agent can walk through an entire listing.
- Prompts live in ``prompts.py`` and structured output models in ``schemas.py``.
"""

from __future__ import annotations

import logging

from strands import Agent

from app.config import settings
from app.model import get_agent_model
from app.prompts import SCRAPER_PROMPT
from app.schemas import ScrapeResult
from app.tools import ALL_TOOLS

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------
def build_scraper_agent() -> Agent:
    """Build the opportunity scraping agent."""
    return Agent(
        model=get_agent_model(),
        tools=ALL_TOOLS,
    )


async def run_scraper(seed_urls: list[str], max_pages: int = 3) -> ScrapeResult:
    """Run the scraping agent against a set of seed listing URLs.

    Args:
        seed_urls (list[str]): Listing pages to start scraping from.
        max_pages (int): Maximum number of pages to visit in one run.

    Returns:
        ScrapeResult: The structured result of the scrape.
    """
    agent = build_scraper_agent()
    prompt = SCRAPER_PROMPT.format(seed_urls=seed_urls, max_pages=max_pages)
    result = await agent.invoke_async(prompt, structured_output_model=ScrapeResult)
    return result.structured_output


if __name__ == "__main__":
    import asyncio

    seeds = [
        "https://opportunitydesk.org/category/fellowships/",
        "https://opportunitydesk.org/category/grants/",
        "https://opportunitydesk.org/category/awards-and-grants/",
        "https://opportunitydesk.org/category/contests/",
        "https://opportunitydesk.org/category/training-and-conference/",
    ]
    asyncio.run(run_scraper(seeds, max_pages=settings.max_pages))