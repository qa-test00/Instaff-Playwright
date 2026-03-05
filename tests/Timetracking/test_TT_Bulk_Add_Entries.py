import pytest
from playwright.sync_api import Page
from tests.pages.time_tracking_page import TimeTrackingPage


@pytest.mark.admin
def test_tt_bulk_add_entries(admin_page: Page):
    """Time Tracking – admin bulk-adds entries for two employees."""
    tt = TimeTrackingPage(admin_page)
    tt.navigate_to_bulk_add()
    tt.bulk_add_entries()
