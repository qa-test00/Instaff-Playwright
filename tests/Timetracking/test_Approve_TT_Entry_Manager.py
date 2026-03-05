import pytest
from playwright.sync_api import Page
from tests.pages.time_tracking_page import TimeTrackingPage


@pytest.mark.admin
def test_approve_tt_entry_manager(admin_page: Page):
    """Time Tracking – manager approves the first pending entry."""
    tt = TimeTrackingPage(admin_page)
    tt.navigate_to_manager()
    tt.approve_first_manager_entry()
