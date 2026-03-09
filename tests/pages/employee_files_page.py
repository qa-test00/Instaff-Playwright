"""
EmployeeFilesPage: actions for the Files module (employee view).
"""
import re
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage
import config


class EmployeeFilesPage(BasePage):
    FILES_URL = f"{config.BASE_URL}/filesv2"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate(self) -> None:
        """Navigate to the Files page via the sidebar link."""
        self.page.get_by_role("link", name="Files").click()
        self.wait_for_load()

    def go_back_to_files(self) -> None:
        """Return to the main Files page."""
        self.page.goto(self.FILES_URL)
        self.wait_for_load()

    def view_folder(self, folder_name: str) -> None:
        """Click the View button on the row matching folder_name."""
        row = self.page.get_by_role("row", name=folder_name)
        row.get_by_role("button", name="View").click()
        self.wait_for_load()

    def view_first_file(self) -> None:
        """Click View on the first file listed in the current folder."""
        self.page.get_by_role("button", name="View").first.click()
        self.wait_for_load()

    def verify_file_opened(self) -> None:
        """Verify that the file opened by checking the page navigated away from filesv2."""
        expect(self.page).not_to_have_url(
            re.compile(r".*/filesv2.*"), timeout=config.DEFAULT_TIMEOUT
        )
