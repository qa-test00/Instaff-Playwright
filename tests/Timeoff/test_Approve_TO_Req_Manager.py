import pytest
from playwright.sync_api import Page
from tests.pages.time_off_page import TimeOffPage


@pytest.mark.admin
def test_approve_to_req_manager(admin_page: Page):
    """Time Off – manager approves the first pending time-off request."""
    to = TimeOffPage(admin_page)
    to.navigate_to_manager()
    to.approve_first_request()
