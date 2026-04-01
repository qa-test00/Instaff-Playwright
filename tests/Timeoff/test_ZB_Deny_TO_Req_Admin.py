import pytest
from playwright.sync_api import Page
from tests.pages.time_off_page import TimeOffPage


@pytest.mark.admin
def test_deny_to_req_admin(admin_page: Page):
    """Time Off – admin cancels the first pending time-off request."""
    to = TimeOffPage(admin_page)
    to.navigate_to_admin()
    to.cancel_first_request()
