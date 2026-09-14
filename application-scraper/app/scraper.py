"""Playwright-based application form fetching.

This module fetches the HTML of an application form page so the agent can
extract the questions and field constraints.
"""

from playwright.async_api import async_playwright


async def fetch_form_html(url: str) -> str:
    """Fetch the HTML content of an application form page.

    Args:
        url: The URL of the application form.

    Returns:
        str: The raw HTML of the page.
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
        html = await page.content()
        await browser.close()
        return html