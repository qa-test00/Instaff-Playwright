import pytest
from datetime import date
from playwright.sync_api import Page
from tests.pages.time_off_page import TimeOffPage


@pytest.mark.employee
def test_to_create_req(employee_page: Page):
    """Time Off – employee creates a new time-off request."""
    today_str = date.today().strftime("%Y-%m-%d")
    comment = f"Regression Test {today_str}"

    to = TimeOffPage(employee_page)

    # Step 1 & 2 – Login as Employee + navigate to Time Off Request page
    to.navigate()

    # Step 3 – Click Create New Request
    to.open_create_modal()

    # Step 4 – Verify PTO is restricted in Type dropdown
    to.verify_pto_restricted()

    # Step 5 – Select Sick in Type dropdown
    to.select_type("Sick")

    # Step 6 – Select date 10 days ahead, then click Done
    to.pick_start_date(days_ahead=10)

    # Step 7 – Input comment
    to.page.locator("#timeoffcomments").fill(comment)

    # Step 8 – Click Add
    to.page.get_by_role("button", name="Add").click()

    # Step 9 – Verify request successfully sent
    to.expect_success_toast()
