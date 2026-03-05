"""
Pytest configuration and shared fixtures for all Playwright tests.
"""
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

import config
from tests.pages.login_page import LoginPage


# ---------------------------------------------------------------------------
# Core browser / context / page fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def playwright():
    """Session-scoped Playwright instance."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright):
    """
    Session-scoped browser instance.
    Re-using a single browser across all tests is faster and avoids the
    overhead of launching a new process per test.
    """
    browser = playwright.chromium.launch(
        headless=config.HEADLESS,
        slow_mo=config.SLOW_MO,
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """
    Function-scoped browser context.
    Each test gets an isolated context (cookies, storage, etc.).
    """
    ctx = browser.new_context(
        permissions=["geolocation"],
        geolocation=config.GEOLOCATION,
    )
    ctx.set_default_timeout(config.DEFAULT_TIMEOUT)
    ctx.set_default_navigation_timeout(config.NAVIGATION_TIMEOUT)
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Function-scoped page – clean slate for every test."""
    p = context.new_page()
    yield p
    p.close()


# ---------------------------------------------------------------------------
# Pre-authenticated page fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def admin_page(page: Page) -> Page:
    """
    A page already logged in as the admin user.
    Use this fixture whenever a test requires admin privileges.
    """
    LoginPage(page).login_as_admin()
    return page


@pytest.fixture(scope="function")
def employee_page(page: Page) -> Page:
    """
    A page already logged in as the employee user.
    Use this fixture whenever a test requires employee privileges.
    """
    LoginPage(page).login_as_employee()
    return page
