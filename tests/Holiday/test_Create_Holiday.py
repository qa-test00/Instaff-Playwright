import json
import pytest
from playwright.sync_api import Page
from tests.pages.holiday_page import HolidayPage

SHARED_DATA_PATH = "shared_data.json"


@pytest.mark.admin
def test_create_holiday(admin_page: Page):
    """Holiday – admin creates a holiday and persists its details for verification."""
    h = HolidayPage(admin_page)
    h.navigate()
    holiday = h.create_holiday(
        name="Regression Testing",
        description="Reg Testing",
        notification="Reg automation testing",
    )

    with open(SHARED_DATA_PATH, "w") as f:
        json.dump([holiday], f, indent=2)
