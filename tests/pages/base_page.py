"""
BasePage: shared helpers used by every page object.
"""
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------

    def wait_for_load(self) -> None:
        """Wait for network to be idle – use sparingly; prefer element waits."""
        self.page.wait_for_load_state("networkidle")

    # ------------------------------------------------------------------
    # Assertion helpers
    # ------------------------------------------------------------------

    def expect_success_toast(self, timeout: int = 15000) -> None:
        """Assert the in-page success notification is visible."""
        expect(self.page.locator("#smallbox1")).to_be_visible(timeout=timeout)
