import pytest
from playwright.sync_api import Page
from tests.pages.time_tracking_page import TimeTrackingPage

EMPLOYEE_ID = 59  # Admin time-tracking employee ID


@pytest.mark.admin
def test_approve_tt_entry_admin(admin_page: Page):
    """Time Tracking – admin approves all awaiting entries for an employee."""
    tt = TimeTrackingPage(admin_page)
    tt.navigate_to_admin_employee(EMPLOYEE_ID)
    tt.approve_all_admin_entries()
