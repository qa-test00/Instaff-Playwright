import pytest
from playwright.sync_api import Page
from tests.pages.time_tracking_page import TimeTrackingPage


@pytest.mark.employee
def test_tt_tbt_entry(employee_page: Page):
    """Time Tracking – employee starts and stops a Track-By-Timer entry."""
    tt = TimeTrackingPage(employee_page)
    tt.navigate()
    tt.navigate_to_timer()
    tt.start_timer(job_num="Job#1", comment="Regression Test")

    # Let the timer run for a moment before stopping
    employee_page.wait_for_timeout(10000)

    tt.stop_timer()
