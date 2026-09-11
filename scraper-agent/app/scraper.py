"""Playwright-based web scraping with pagination support.

This module handles the low-level browser automation for the opportunity
scraping agent. It fetches listing pages (and their paginated pages) and
returns the raw HTML documents for further processing.
"""

from typing import List

from bs4 import BeautifulSoup
from playwright.async_api import Page, async_playwright


async def scrape_webpage(url: str, is_paginated: bool = False, max_pages: int = 3) -> List[str]:
    """Scrape a webpage, handling pagination if necessary.

    Args:
        url: The URL of the webpage to scrape.
        is_paginated: Whether the webpage is paginated.
        max_pages: Maximum number of pages to scrape when paginated.

    Returns:
        A list of HTML documents, one for each page.
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--single-process",
            ],
        )
        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=0)

        if is_paginated:
            documents = await _scrape_paginated(page, max_pages=max_pages)
        else:
            documents = [await _scrape_single_page(page)]

        await browser.close()
        return documents


async def _scrape_single_page(page: Page) -> str:
    """Scrape the content of a single page."""
    return await page.content()


async def _scrape_paginated(page: Page, max_pages: int = 3) -> List[str]:
    """Scrape a paginated listing by following the numbered page links.

    This handles WordPress-style pagination where page 2 is at
    ``/page/2/`` and there is a "Next" link. It walks through pages by
    clicking the "Next" link until it no longer exists or ``max_pages``
    is reached.
    """
    documents = []
    for _ in range(max_pages):
        document = await _scrape_single_page(page)
        documents.append(document)

        # Look for a "Next" link to advance to the following page
        next_link = await page.query_selector("a.next, a[rel='next'], a:has-text('Next')")
        if not next_link:
            break
        try:
            await next_link.click()
            await page.wait_for_load_state(state="domcontentloaded", timeout=0)
        except Exception:
            break
    return documents


def extract_detail_links(html: str, base_url: str) -> list[str]:
    """Extract opportunity detail page URLs from a listing page's HTML.

    Detail pages on opportunitydesk.org follow the pattern
    ``/YYYY/MM/DD/slug/``. We filter out category, tag, author, and
    pagination links.

    Args:
        html: The raw HTML of the listing page.
        base_url: The base URL used to resolve relative links.

    Returns:
        A list of absolute detail page URLs.
    """
    soup = BeautifulSoup(html, "html.parser")
    links: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith("#") or href.startswith("mailto:"):
            continue
        # Skip internal navigation links
        if any(seg in href for seg in ("/category/", "/tag/", "/author/", "/page/", "?page=")):
            continue
        if href.startswith("/"):
            href = base_url.rstrip("/") + href
        # Only keep links that look like dated detail pages
        if "/20" in href and href.startswith("http") and "opportunitydesk.org" in href:
            links.add(href)
    return list(links)