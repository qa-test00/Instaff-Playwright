"""
Pytest configuration and fixtures for Playwright tests.
"""
import os
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def playwright():
    """Session-scoped Playwright instance."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="function")
def browser(playwright):
    """Function-scoped browser instance."""
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    """Function-scoped browser context with geolocation permissions."""
    context = browser.new_context(
        permissions=["geolocation"],
        geolocation={"latitude": 37.7749, "longitude": -122.4194},
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """Function-scoped page instance."""
    page = context.new_page()
    yield page
    page.close()
