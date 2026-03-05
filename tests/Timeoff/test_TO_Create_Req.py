import pytest
from playwright.sync_api import Page
from tests.pages.time_off_page import TimeOffPage


@pytest.mark.employee
def test_to_create_req(employee_page: Page):
    """Time Off – employee creates a new time-off request."""
    to = TimeOffPage(employee_page)
    to.navigate()
    to.create_request(comment="Regression Test")
