import pytest
from playwright.sync_api import Page
from tests.pages.time_off_page import TimeOffPage


@pytest.mark.employee
def test_to_time_restriction(john_page: Page):
    """Time Off – verify PTO type is restricted for john employee."""
    to = TimeOffPage(john_page)
    to.navigate()
    to.open_create_modal()
    to.verify_pto_restricted()
    to.close_modal()
