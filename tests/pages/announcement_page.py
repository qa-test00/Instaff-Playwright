"""
AnnouncementPage: actions for the Announcements module.
"""
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage


class AnnouncementPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # Admin navigation
    def navigate_admin(self) -> None:
        self.page.get_by_role("link", name="Announcements", exact=True).click()
        self.wait_for_load()

    # Employee navigation
    def navigate_employee(self) -> None:
        self.page.get_by_role("link", name=" Announcements").click()
        self.wait_for_load()

    def create_announcement(self, title: str = "Regression Testing") -> None:
        self.page.locator("#title").fill(title)
        self.page.get_by_role("textbox", name="Select a date").click()
        self.page.get_by_title("Next Month").click()
        self.page.get_by_role("cell", name="2").first.click()
        self.page.get_by_role("button", name="Confirm").click()
        self.page.get_by_role("button", name="Add Announcement").click()
        self.wait_for_load()
        self.expect_success_toast()

    def delete_first_announcement(self) -> None:
        # Expand the first announcement panel (DB-based IDs vary; use the toggle link)
        self.page.locator("a[data-toggle='collapse']").first.click()
        self.page.wait_for_timeout(500)
        self.page.get_by_role("button", name="Delete").first.click()
        self.wait_for_load()
        self.page.get_by_role("button", name="Delete Announcement").click()
        self.wait_for_load()
        self.expect_success_toast()
