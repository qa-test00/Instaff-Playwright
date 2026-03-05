import pytest
from playwright.sync_api import Page, expect
from tests.pages.time_tracking_page import TimeTrackingPage


@pytest.mark.admin
def test_tt_reports(admin_page: Page):
    """Time Tracking – admin builds a report and verifies the table is populated."""
    tt = TimeTrackingPage(admin_page)
    tt.navigate_to_reports()
    tt.build_tt_report(
        employee_search="auto employee",
        department="IT",
        task="Deployment/Support/Calls",
    )
    expect(admin_page.locator("#dt_basic tbody tr").first).to_be_visible()
