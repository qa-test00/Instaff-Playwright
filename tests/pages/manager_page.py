"""
ManagerPage: actions for the Manager module (employee files, paystubs, tax forms).
"""
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage
import config


class ManagerPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate_employees(self) -> None:
        self.page.get_by_role("link", name=" Manager ").click()
        self.page.get_by_role("link", name="My Employees").click()
        self.wait_for_load()

    def open_employee_menu(self, employee_row_name: str) -> None:
        self.page.get_by_role("row", name=employee_row_name).get_by_role("button").click()

    def view_paystubs(self, employee_row_name: str) -> None:
        self.open_employee_menu(employee_row_name)
        self.page.get_by_role("link", name="See Paystubs").click()
        self.wait_for_load()
        self.page.get_by_role("button", name="View").first.click()
        expect(self.page.locator("#pdfViewer div").nth(1)).to_be_visible(
            timeout=config.DEFAULT_TIMEOUT
        )

    def view_tax_forms(self, employee_row_name: str) -> None:
        # Navigate back to the employee list before clicking again
        self.page.goto(f"{config.BASE_URL}/manager/employees")
        self.wait_for_load()
        self.open_employee_menu(employee_row_name)
        self.page.get_by_role("link", name="See Tax Forms").click()
        self.wait_for_load()
        expect(self.page.locator("h2")).to_be_visible()
