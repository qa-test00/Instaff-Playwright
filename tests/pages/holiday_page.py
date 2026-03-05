"""
HolidayPage: actions for the Holiday management module.
"""
from datetime import datetime
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage


class HolidayPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate(self) -> None:
        self.page.get_by_role("link", name="Holidays", exact=True).click()
        self.wait_for_load()

    def create_holiday(
        self,
        name: str = "Regression Testing",
        description: str = "Reg Testing",
        notification: str = "Reg automation testing",
    ) -> dict:
        """Create a holiday and return a dict with name and formatted date."""
        self.page.get_by_text("Create New Holiday").click()
        self.page.locator("#holidayname").fill(name)
        self.page.locator("#description").click()

        # Read back the auto-populated date before filling description
        holiday_name = self.page.locator("#holidayname").input_value().strip()
        raw_date = self.page.locator("#start-time").input_value().strip()
        formatted_date = datetime.strptime(raw_date, "%B %d, %Y").strftime("%B %d, %Y")

        self.page.locator("#description").fill(description)
        self.page.locator("#notification").fill(notification)
        self.page.get_by_role("button", name="Submit").click()
        self.wait_for_load()
        self.expect_success_toast()

        return {"holiday_Name": holiday_name, "date": formatted_date}

    def delete_first_holiday(self) -> None:
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.get_by_role("button", name="Delete").first.click()
        self.expect_success_toast()

    def get_holiday_list_items(self):
        """Return the Locator for all holiday rows in the holidays table."""
        return self.page.locator("#holidays-table tbody tr")
