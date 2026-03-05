"""
TimeTrackingPage: actions for the Time Tracking module.
"""
from datetime import date
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage
import config


class TimeTrackingPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ------------------------------------------------------------------
    # Employee – Data Entry
    # ------------------------------------------------------------------

    def navigate(self) -> None:
        self.page.locator("a[href='/timetracking']").first.click()
        self.wait_for_load()

    def fill_data_entry(self, hours: str = "8", comment: str = "Reg Test") -> None:
        self.page.locator("#hours").fill(hours)
        self.page.locator("#taskdate").click()
        self.page.locator(".datepicker th.next").first.click()
        self.page.locator(".datepicker td.day:not(.old):not(.new)").filter(has_text="10").first.click()
        self.page.locator("#comments").fill(comment)
        self.page.get_by_role("button", name="Add Selected").click()
        self.expect_success_toast()

    def navigate_to_unsubmitted(self) -> None:
        self.page.get_by_role("link", name="Unsubmitted Entries").click()
        self.wait_for_load()

    def get_first_unsubmitted_date(self) -> str:
        date_cell = self.page.locator(
            "#dt_basic_unsubmitted > tbody > tr:nth-child(1) > td:nth-child(1)"
        )
        date_cell.wait_for(state="visible")
        return date_cell.text_content().strip()

    def submit_entry(self, row_name: str) -> None:
        self.page.locator("#checkAllUnsubmitted").uncheck()
        self.page.get_by_role("row", name=row_name).locator(
            "#unsubmitted_entry_checkbox"
        ).first.check()
        self.page.get_by_role("checkbox", name="I Certify That All Above Time").check()
        self.page.get_by_role("button", name="Submit Selected Entries To").click()
        self.expect_success_toast()

    # ------------------------------------------------------------------
    # Employee – Track By Timer
    # ------------------------------------------------------------------

    def navigate_to_timer(self) -> None:
        self.page.locator("a").filter(has_text="Track By Timer").click()
        self.wait_for_load()

    def start_timer(self, job_num: str = "Job#1", comment: str = "Regression Test") -> None:
        self.page.locator("#jobnum_timer").fill(job_num)
        self.page.locator("#comments_timer").fill(comment)
        self.page.once("dialog", lambda d: d.accept())
        self.page.locator(
            "#tt_new_entry_timer > fieldset > div.form-actions > div > div > button"
        ).click()

    def stop_timer(self) -> None:
        stop_btn = self.page.get_by_role("button", name="Stop Timer").first
        expect(stop_btn).to_be_visible()
        # Extract the timer ID from the button's onclick attribute, then submit the form directly
        onclick = stop_btn.get_attribute("onclick")
        timer_id = onclick.split("`")[1] if onclick else None
        if timer_id:
            self.page.evaluate(f"""
                var form = document.getElementById('stopWatchForm_{timer_id}');
                if (form) {{
                    var lat = document.getElementById('latitude_{timer_id}');
                    var lng = document.getElementById('longitude_{timer_id}');
                    if (lat) lat.value = '37.7749';
                    if (lng) lng.value = '-122.4194';
                    form.submit();
                }}
            """)
        else:
            stop_btn.click()
        self.wait_for_load()

    # ------------------------------------------------------------------
    # Manager approval
    # ------------------------------------------------------------------

    def navigate_to_manager(self) -> None:
        self.page.locator("a[href='/timetracking']").first.click()
        self.page.get_by_role("link", name=" Manager").click()
        self.wait_for_load()

    def _dismiss_modal_if_present(self) -> None:
        """Press Escape up to 3 times to close any overlay dialogs."""
        for _ in range(3):
            try:
                self.page.keyboard.press("Escape")
                self.page.wait_for_timeout(500)
            except Exception:
                break

    def approve_first_manager_entry(self) -> None:
        self.page.get_by_role("link", name="View").nth(1).click()
        self._dismiss_modal_if_present()
        self.page.get_by_role("checkbox").nth(1).check()
        self.page.get_by_role("button", name="Approve Selected Entries").click()
        self._dismiss_modal_if_present()
        self.expect_success_toast()

    # ------------------------------------------------------------------
    # Admin approval
    # ------------------------------------------------------------------

    def navigate_to_admin_employee(self, employee_id: int) -> None:
        self.page.goto(f"{config.BASE_URL}/admin/timetracking/{employee_id}")
        self.wait_for_load()

    def approve_all_admin_entries(self) -> None:
        self.page.locator(
            "input[name='entries_checkboxes_admin_awaiting_approval']"
        ).check()
        self.wait_for_load()
        self.page.get_by_role("button", name="Approve Selected Entries").click()
        self.expect_success_toast()

    # ------------------------------------------------------------------
    # Admin – Reports
    # ------------------------------------------------------------------

    def _select_from_selectize(self, input_id: str, search_text: str) -> None:
        """Click a selectize input, type to filter, then click the first matching option."""
        self.page.locator(input_id).click()
        self.page.locator(input_id).fill(search_text)
        self.page.locator(".selectize-dropdown-content .option").first.click()

    def navigate_to_reports(self) -> None:
        self.page.goto(f"{config.BASE_URL}/admin/timetracking/reports")
        self.wait_for_load()

    def build_tt_report(self, employee_search: str, department: str, task: str) -> None:
        self._select_from_selectize("#employeeid-selectized", employee_search)
        self.page.select_option("#deptid", label=department)
        self.page.select_option("#taskid", label=task)
        self.page.get_by_role("button", name="Build Report").click()
        self.wait_for_load()

    # ------------------------------------------------------------------
    # Admin – Bulk Add Entries
    # ------------------------------------------------------------------

    def navigate_to_bulk_add(self) -> None:
        self.page.goto(f"{config.BASE_URL}/admin/timetracking/bulk-entries")
        self.wait_for_load()

    def _fill_bulk_row(self, row_index: int, employee_search: str, hours: str = "8") -> None:
        """Fill one row in the Bulk Add Entries form (0-based index)."""
        suffix = "" if row_index == 0 else f"-{row_index}"
        today_day = str(date.today().day)

        # Task dropdown — selecting a task triggers the employee dropdown to load
        self.page.locator(f"#taskid{suffix}").select_option(label="Deployment/Support/Calls")
        self.page.wait_for_timeout(500)

        # Date picker modal: click the input, pick today, confirm
        self.page.locator(f"#taskdate{suffix}").click()
        self.page.locator(".datepicker td.day:not(.old):not(.new)").filter(
            has_text=today_day
        ).first.click()
        self.page.locator(".modal-datepicker-confirm").click()

        # Employee — Magic Suggest widget (requires real keystrokes to trigger search)
        emp_dd = self.page.locator(f"#employeeNameAndIdDD{suffix}")
        emp_dd.click()
        emp_dd.locator("input").press_sequentially(employee_search, delay=80)
        self.page.locator(".ms-res-item").first.click()

        # Regular Hours
        self.page.locator(f"#hours{suffix}").fill(hours)

    def bulk_add_entries(self) -> None:
        """Fill two rows and submit the Bulk Add Entries form."""
        self._fill_bulk_row(0, "AUTOEMP")
        self.page.locator("#add-new-row-btn").click()
        self.page.wait_for_timeout(500)
        self._fill_bulk_row(1, "100050")
        with self.page.expect_navigation():
            self.page.locator("#addSelectedNewEntryBtnId").click()
        # Successful submit resets the form (task dropdown is cleared)
        expect(self.page.locator("#taskid")).to_have_value("")

    # ------------------------------------------------------------------
    # Admin – Attendance Time Report
    # ------------------------------------------------------------------

    def navigate_to_attendance_report(self) -> None:
        self.page.goto(f"{config.BASE_URL}/admin/timetracking/attendance_report")
        self.wait_for_load()

    def build_attendance_report(self, employee_search: str) -> None:
        self._select_from_selectize("#employeeid-selectized", employee_search)
        self.page.get_by_role("button", name="Build Report").click()
        self.wait_for_load()
