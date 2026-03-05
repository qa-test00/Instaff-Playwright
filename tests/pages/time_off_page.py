"""
TimeOffPage: actions for the Time Off module.
"""
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage
import config


class TimeOffPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ------------------------------------------------------------------
    # Employee – Create request
    # ------------------------------------------------------------------

    def navigate(self) -> None:
        self.page.get_by_role("link", name=" Time Off Request").click()
        self.wait_for_load()

    def create_request(self, comment: str = "Regression Test") -> None:
        self.page.get_by_role("button", name="Create New Request").click()
        self.page.locator("#timeoffcomments").fill(comment)
        self.page.get_by_role("button", name="Add").click()
        self.expect_success_toast()

    # ------------------------------------------------------------------
    # Manager – Approve request
    # ------------------------------------------------------------------

    def navigate_to_manager(self) -> None:
        self.page.goto(
            f"{config.BASE_URL}/manager/timeoff?next=/manager/timeoff"
        )
        self.wait_for_load()

    def approve_first_request(self) -> None:
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.get_by_role("button", name="Approve").click()
        expect(self.page.locator("#smallbox1")).to_be_visible(timeout=15000)

    # ------------------------------------------------------------------
    # Admin – Cancel / deny request
    # ------------------------------------------------------------------

    def navigate_to_admin(self) -> None:
        self.page.get_by_role("link", name="Time Off Requests ").click()
        self.page.get_by_role("link", name="Time Off Manager").click()
        self.wait_for_load()

    def cancel_first_request(self) -> None:
        cancel_btn = self.page.get_by_role("button", name="Cancel Request").first
        row = cancel_btn.locator("xpath=ancestor::tr")

        self.page.once("dialog", lambda dialog: dialog.accept())
        cancel_btn.click()

        # Handle in-page confirmation modals if the dialog handler didn't fire
        for selector in (
            self.page.get_by_role("button", name="Ok", exact=True),
            self.page.get_by_role("button", name="OK", exact=True),
            self.page.get_by_role("button", name="Yes", exact=True),
            self.page.get_by_role("button", name="Confirm", exact=True),
            self.page.get_by_role("button", name="Cancel Request", exact=True),
        ):
            try:
                selector.click(timeout=3000)
                break
            except Exception:
                pass

        self.wait_for_load()
        expect(row.get_by_role("button", name="Cancel Request")).to_be_hidden(
            timeout=15000
        )

    # ------------------------------------------------------------------
    # Admin – Reports
    # ------------------------------------------------------------------

    def navigate_to_reports(self) -> None:
        self.page.get_by_role("link", name="Time Off Requests ").click()
        self.page.get_by_role("link", name="Reports").click()
        self.wait_for_load()

    def generate_report(self, employee_search: str) -> None:
        import re
        self.page.locator("div").filter(has_text=re.compile(r"^All$")).first.click()
        self.page.locator("#employeeid-selectized").fill(employee_search)
        self.page.locator("#employeeid-selectized").press("Enter")
        self.page.get_by_role("button", name="Build Report").click()
