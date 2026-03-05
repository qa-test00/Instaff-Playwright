import pytest
from playwright.sync_api import Page
from tests.pages.time_tracking_page import TimeTrackingPage


@pytest.mark.employee
def test_tt_data_entry(employee_page: Page):
    """Time Tracking – employee submits a regular data entry."""
    tt = TimeTrackingPage(employee_page)
    tt.navigate()
    tt.fill_data_entry(hours="8", comment="Reg Test")

    tt.navigate_to_unsubmitted()
    entry_date = tt.get_first_unsubmitted_date()

    row_name = f"{entry_date} Reg Test 8.00"
    tt.submit_entry(row_name)
