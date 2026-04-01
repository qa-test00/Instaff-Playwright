import pytest
from datetime import date
from playwright.sync_api import Page
from tests.pages.time_off_page import TimeOffPage


@pytest.mark.admin
def test_to_mgr_add_req_for_employee(admin_page: Page):
    """Time Off – manager adds a request for employee via /manager/timeoff,
    verifies calendar & table, then cancels."""
    comment = f"Regression Testing ({date.today().strftime('%B %d, %Y')})"
    to = TimeOffPage(admin_page)

    # Step 3-9: Navigate to /manager/timeoff and add request for AUTOEMP
    to.navigate_to_manager_timeoff()
    to.add_manager_request_for_employee(comment=comment, days_ahead=15)

    # Step 10: Go back to /manager/timeoff and verify entry on calendar and Approved & Upcoming table
    to.navigate_to_manager_timeoff()
    to.verify_calendar_entry("Auto Employee")
    to.verify_upcoming_table_entry("Auto Employee")

    # Steps 11-12: Navigate to Time Off Manager then cancel
    to.navigate_to_admin()
    to.cancel_first_request()
