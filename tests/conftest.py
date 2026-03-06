"""
Pytest configuration and shared fixtures for all Playwright tests.
"""
import re
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

import config
from tests.pages.login_page import LoginPage


# ---------------------------------------------------------------------------
# Screenshot on failure
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach rep_* attributes to the item and take a screenshot on failure."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call" and rep.failed:
        # Try to find any live Page object from the test's fixtures.
        page = None
        for fixture_name in ("page", "admin_page", "employee_page", "john_page"):
            page = item.funcargs.get(fixture_name)
            if page is not None:
                break

        if page is not None:
            screenshots_dir = Path("reports/screenshots")
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            safe_name = re.sub(r"[^\w\-]", "_", item.nodeid)
            screenshot_path = screenshots_dir / f"{safe_name}.png"
            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                # Store path on item so the summary report can reference it.
                item.screenshot_path = str(screenshot_path)
            except Exception:
                pass


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


@pytest.fixture(scope="function")
def john_page(page: Page) -> Page:
    """
    A page already logged in as marben+john@hutility.com.
    Used for time-restriction tests.
    """
    LoginPage(page).login("marben+john@hutility.com", "Temp1234!!")
    return page
