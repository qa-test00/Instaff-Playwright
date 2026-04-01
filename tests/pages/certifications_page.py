"""
CertificationsPage: actions for the Certifications module.
"""
from datetime import date, timedelta
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage


class CertificationsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate(self) -> None:
        self.page.get_by_role("link", name="Certifications").click()
        self.wait_for_load()

    def open_add_certificate_modal(self) -> None:
        self.page.get_by_role("button", name="Add New Certificate").click()
        self.page.wait_for_selector("#requestModal", state="visible")

    def select_type_with_custom_fields(self) -> None:
        self.page.locator("#certificationid").select_option(label="With Custom Fields")
        # Wait for custom fields to render in #customFieldsContainer
        self.page.wait_for_selector("#customfield2value", state="visible")

    def verify_required_field_is_required(self) -> None:
        expect(self.page.locator("#customfield2value")).to_have_attribute("required", "")

    def verify_non_required_field_is_not_required(self) -> None:
        expect(self.page.locator("#customfield3value")).not_to_have_attribute("required", "")

    def fill_add_certificate_form(
        self,
        required_value: str,
        file_path: str,
        days_ahead: int = 10,
    ) -> None:
        target_date = date.today() + timedelta(days=days_ahead)

        self.page.locator("#customfield2value").fill(required_value)

        # Open the Bootstrap Datetimepicker; clear first so it always opens in day view
        self.page.locator("#expiry").fill("")
        self.page.locator("#expiry").click()
        self.page.wait_for_selector(".datepicker-days", state="visible")

        target_month_year = target_date.strftime("%B %Y")  # e.g. "March 2026"
        target_data_day = target_date.strftime("%m/%d/%Y")  # e.g. "03/16/2026"

        # Navigate forward until the correct month is shown (scoped to the day-view table)
        while True:
            current_header = self.page.locator(".datepicker-days th.picker-switch").inner_text()
            if current_header.strip() == target_month_year:
                break
            self.page.locator(".datepicker-days th.next").click()

        # Click the target day (force=True avoids detached-DOM retries from datepicker re-renders)
        self.page.locator(f'.datepicker-days td[data-action="selectDay"][data-day="{target_data_day}"]').click(force=True)
        
        self.page.locator("#file").set_input_files(file_path)
        # S3 redirects to http:// which returns 404 on staging; intercept and fix to https://
        self.page.route(
            "http://marben.staging.instaff.org/certification_uploaded_employee**",
            lambda route: route.fulfill(
                status=302,
                headers={"Location": route.request.url.replace("http://", "https://", 1)},
            ),
        )
        self.page.locator("#AddBtn").click()

    def verify_upload_successful(self) -> None:
        # Wait for Django to process the upload and redirect back to /certifications
        self.page.wait_for_url(lambda url: "/certifications" in url and "certification_uploaded_employee" not in url, timeout=30000)
        expect(self.page.get_by_text("Upload successful")).to_be_visible(timeout=15000)

    def click_view_button(self, cert_name: str) -> None:
        self.page.locator("table tr").filter(has_text=cert_name).get_by_role("button", name="View").click()
        self.page.wait_for_selector("#pdfViewer", state="visible")

    def verify_pdf_viewer_displayed(self, filename: str) -> None:
        from playwright.sync_api import expect
        expect(self.page.locator("#pdfViewer")).to_be_visible()
        expect(self.page.locator("#pdf_title")).to_contain_text(filename)
        expect(self.page.locator("#pdf_iframe")).to_be_visible()

    def click_pending_tab(self) -> None:
        self.page.locator("a[href='#tab-pending']").click()
        self.wait_for_load()

    def verify_certificate_in_pending(self, required_value: str) -> None:
        expect(
            self.page.locator("#tab-pending").locator("table tr").filter(has_text=required_value).first
        ).to_be_visible(timeout=15000)

    # ------------------------------------------------------------------
    # Admin – Approve pending certifications
    # ------------------------------------------------------------------

    def navigate_admin(self) -> None:
        self.page.goto("https://marben.staging.instaff.org/admin/certifications")
        self.wait_for_load()

    def click_pending_employee_records_tab(self) -> None:
        self.page.locator("a[href='#tab-employees-pending']").click()
        self.page.wait_for_timeout(800)

    def check_first_pending_record(self) -> None:
        self.page.locator("input[name='pending_records_checkboxes']").first.check()

    def check_pending_record_for_employee(self, employee_name: str) -> None:
        self.page.locator("tr").filter(has_text=employee_name).locator(
            "input[name='pending_records_checkboxes']"
        ).first.check()

    def click_approve_selected(self) -> None:
        self.page.get_by_role("button", name="Approve Selected").click()
        self.page.wait_for_selector("#approveModal", state="visible")

    def confirm_approve(self) -> None:
        self.page.locator("#mass-approve-button").click()
        self.expect_success_toast()

    # ------------------------------------------------------------------
    # Admin – Delete employee certification record
    # ------------------------------------------------------------------

    def click_details_for_cert(self, cert_name: str) -> None:
        self.page.locator("tr").filter(has_text=cert_name).get_by_role("link", name="Details").click()
        self.wait_for_load()

    def click_employee_records_tab(self) -> None:
        self.page.locator("a[href='#tab-employees']").click()
        self.page.wait_for_selector("#tab-employees.active", state="attached", timeout=10000)
        self.wait_for_load()
        self.page.wait_for_selector("#employee_records_table tbody tr", state="visible")

    def search_employee_records(self, search_term: str) -> None:
        self.page.locator("#employee_records_table_filter input[type='search']").fill(search_term)
        self.page.wait_for_timeout(2000)

    def click_edit_for_employee(self, employee_name: str) -> None:
        self.page.locator("#employee_records_table tbody tr").filter(has_text=employee_name).get_by_role("link", name="Edit").click()
        self.wait_for_load()

    def click_delete_record_button(self) -> None:
        self.page.get_by_role("button", name="Delete Record?").click()
        self.page.wait_for_selector("#deleteModal", state="visible")

    def enter_admin_password(self, password: str) -> None:
        self.page.locator("#admin_pw").fill(password)

    def click_delete_confirm(self) -> None:
        self.page.locator("#delete-button").click()
        self.wait_for_load()

    def verify_delete_success(self) -> None:
        self.expect_success_toast()
