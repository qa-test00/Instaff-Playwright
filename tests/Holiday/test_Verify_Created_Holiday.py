import json
import os
import pytest
from playwright.sync_api import Page
from tests.pages.holiday_page import HolidayPage

SHARED_DATA_PATH = "shared_data.json"


@pytest.fixture(scope="module")
def holidays():
    if not os.path.exists(SHARED_DATA_PATH):
        pytest.skip(f"Shared data file not found: {SHARED_DATA_PATH}")
    with open(SHARED_DATA_PATH) as f:
        return json.load(f)


@pytest.mark.admin
def test_verify_created_holiday(admin_page: Page, holidays):
    """Holiday – verify the created holiday appears in the list with correct details."""
    h = HolidayPage(admin_page)
    h.navigate()

    items = h.get_holiday_list_items()
    count = items.count()

    assert count == len(holidays), (
        f"Expected {len(holidays)} holiday(s) in the list, found {count}"
    )

    for i, holiday in enumerate(holidays):
        row = items.nth(i)
        actual_name = row.locator("td[data-col='holiday-name']").inner_text().strip()
        actual_date = row.locator("td[data-col='start-time']").inner_text().strip()
        assert actual_name == holiday["holiday_Name"], (
            f"Row {i}: expected name '{holiday['holiday_Name']}', got '{actual_name}'"
        )
        assert actual_date == holiday["date"], (
            f"Row {i}: expected date '{holiday['date']}', got '{actual_date}'"
        )
