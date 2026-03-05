"""
LoginPage: handles the login form.
"""
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage
import config


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._email = page.get_by_role("textbox", name="Enter your email address")
        self._password = page.get_by_role("textbox", name="Enter your password")
        self._login_btn = page.get_by_role("button", name="Log In")

    def goto(self) -> None:
        self.page.goto(config.LOGIN_URL)

    def login(self, email: str, password: str) -> None:
        self.goto()
        self._email.fill(email)
        self._email.press("Tab")
        self._password.fill(password)
        self._login_btn.click()
        # Wait for the page to finish navigating after login
        self.page.wait_for_url(lambda url: "/login" not in url, timeout=config.NAVIGATION_TIMEOUT)

    def login_as_admin(self) -> None:
        self.login(config.ADMIN_EMAIL, config.ADMIN_PASSWORD)

    def login_as_employee(self) -> None:
        self.login(config.EMPLOYEE_EMAIL, config.EMPLOYEE_PASSWORD)
