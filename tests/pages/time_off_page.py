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

    def open_create_modal(self) -> None:
        self.page.get_by_role("button", name="Create New Request").click()
        self.page.wait_for_selector(".modal", state="visible")

    def verify_pto_restricted(self) -> None:
        """Assert that the PTO option is disabled in the Type dropdown."""
        from playwright.sync_api import expect
        pto_option = self.page.locator("#timeofftypeid option[disabled]:has-text('PTO')")
        expect(pto_option).to_have_attribute("disabled", "", timeout=10000)

    def close_modal(self) -> None:
        self.page.keyboard.press("Escape")

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
    # Manager – Add request for employee
    # ------------------------------------------------------------------

    def navigate_to_manager_timeoff(self) -> None:
        self.page.goto(f"{config.BASE_URL}/manager/timeoff")
        self.wait_for_load()

    def add_manager_request_for_employee(self, comment: str) -> None:
        self.page.goto(f"{config.BASE_URL}/manager/timeoff/add")
        self.wait_for_load()
        self.page.locator("#employee_id").select_option(label="Auto Employee (AUTOEMP)")
        self.page.locator("#timeofftypeid").select_option(label="Holiday")
        self.page.locator("#timeoffcomments").fill(comment)
        self.page.get_by_role("button", name="Add").click()
        self.expect_success_toast()

    # ------------------------------------------------------------------
    # Admin – Add request for employee
    # ------------------------------------------------------------------

    def navigate_to_admin_timeoff(self) -> None:
        self.page.goto(f"{config.BASE_URL}/admin/timeoff")
        self.wait_for_load()

    def add_request_for_employee(self, comment: str) -> None:
        self.page.goto(f"{config.BASE_URL}/admin/timeoff/add")
        self.wait_for_load()
        self.page.locator("#employee_id").select_option(label="Auto Employee (AUTOEMP)")
        self.page.locator("#timeofftypeid").select_option(label="Holiday")
        self.page.locator("#timeoffcomments").fill(comment)
        self.page.get_by_role("button", name="Add").click()
        self.expect_success_toast()

    def verify_calendar_entry(self, employee_name: str) -> None:
        # Wait for FullCalendar to finish rendering events via AJAX
        self.page.wait_for_selector(".fc-event", state="visible", timeout=15000)
        expect(
            self.page.locator(".fc-event").filter(has_text=employee_name).first
        ).to_be_visible(timeout=15000)

    def verify_upcoming_table_entry(self, employee_name: str) -> None:
        expect(
            self.page.locator("table tr").filter(has_text=employee_name).first
        ).to_be_visible(timeout=15000)

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

    # ------------------------------------------------------------------
    # Admin – Print / Download Calendar
    # ------------------------------------------------------------------

    def print_calendar_to_pdf(self) -> str:
        """Click 'Print Calendar To PDF', wait for the download, and return the filename."""
        with self.page.expect_download() as dl_info:
            self.page.get_by_role("button", name="Print Calendar To PDF").click()
        download = dl_info.value
        assert download.suggested_filename.lower().endswith(".pdf"), (
            f"Expected a .pdf file but got: {download.suggested_filename}"
        )
        return download.suggested_filename

    def download_calendar_ical(self) -> str:
        """Click 'Download Calendar (iCal Format)', wait for the download, and return the filename."""
        with self.page.expect_download() as dl_info:
            self.page.get_by_role("button", name="Download Calendar (iCal Format)").click()
        download = dl_info.value
        assert download.suggested_filename.lower().endswith(".ics"), (
            f"Expected a .ics file but got: {download.suggested_filename}"
        )
        return download.suggested_filename
