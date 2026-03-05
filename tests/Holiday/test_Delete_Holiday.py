import pytest
from playwright.sync_api import Page
from tests.pages.holiday_page import HolidayPage


@pytest.mark.admin
def test_delete_holiday(admin_page: Page):
    """Holiday – admin deletes the first holiday in the list."""
    h = HolidayPage(admin_page)
    h.navigate()
    h.delete_first_holiday()
