import pytest
from datetime import date
from playwright.sync_api import Page
from tests.pages.time_off_page import TimeOffPage


@pytest.mark.admin
def test_to_add_req_for_employee(admin_page: Page):
    """Time Off – admin adds a request for employee, verifies calendar & table, then cancels."""
    comment = f"Regression Testing ({date.today().strftime('%B %d, %Y')})"
    to = TimeOffPage(admin_page)

    # Step 3-9: Navigate to /admin/timeoff and add request for AUTOEMP
    to.navigate_to_admin_timeoff()
    to.add_request_for_employee(comment=comment)

    # Step 10: Go back to /admin/timeoff and verify entry on calendar and Approved & Upcoming table
    to.navigate_to_admin_timeoff()
    to.verify_calendar_entry("Auto Employee")
    to.verify_upcoming_table_entry("AUTOEMP")

    # Steps 11-12: Cancel the request and approve the confirmation
    to.cancel_first_request()
