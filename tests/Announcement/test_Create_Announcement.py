import pytest
from playwright.sync_api import Page
from tests.pages.announcement_page import AnnouncementPage


@pytest.mark.admin
def test_create_announcement(admin_page: Page):
    """Announcement – admin creates a new announcement."""
    ann = AnnouncementPage(admin_page)
    ann.navigate_admin()
    ann.create_announcement(title="Regression Testing")
