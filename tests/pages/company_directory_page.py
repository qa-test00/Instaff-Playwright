"""
CompanyDirectoryPage: actions for the Company Directory module.
"""
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage


class CompanyDirectoryPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate(self) -> None:
        self.page.get_by_role("link", name=" Company Directory").click()
        self.wait_for_load()

    def navigate_org_chart(self) -> None:
        self.page.get_by_role("link", name=" Organization Chart").click()
        self.wait_for_load()

    def add_position(
        self,
        title: str,
        description: str,
        department_option: str,
        reports_to_option: str,
    ) -> None:
        self.page.get_by_role("button", name=" Add Position").click()
        self.wait_for_load()
        expect(self.page.get_by_role("heading", name="Add New Position")).to_be_visible()
        self.page.get_by_role("textbox", name="Position Title *").fill(title)
        self.page.get_by_role("textbox", name="Description").fill(description)
        self.page.get_by_role("dialog", name="Add New Position").get_by_label(
            "Department"
        ).select_option(department_option)
        self.page.get_by_label("Reports To").select_option(reports_to_option)
        self.page.get_by_role("button", name=" Create Position").click()
        self.wait_for_load()
        expect(
            self.page.locator("div").filter(has_text="Position created").nth(1)
        ).to_be_visible()

    def delete_position(self, nth: int = 4) -> None:
        self.page.get_by_role("button", name=" Edit").nth(nth).click()
        self.wait_for_load()
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.get_by_role("button", name=" Delete Position").click()
