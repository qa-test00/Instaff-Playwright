import pytest
from playwright.sync_api import Page, expect
from tests.pages.time_tracking_page import TimeTrackingPage


@pytest.mark.admin
def test_tt_attendance_report(admin_page: Page):
    """Time Tracking – admin builds an attendance time report and verifies the summary table."""
    tt = TimeTrackingPage(admin_page)
    tt.navigate_to_attendance_report()
    tt.build_attendance_report(employee_search="auto employee")
    expect(admin_page.locator("table.k-selectable tbody tr").first).to_be_visible(timeout=15000)
