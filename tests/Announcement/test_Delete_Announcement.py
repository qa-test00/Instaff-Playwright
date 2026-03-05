import pytest
from playwright.sync_api import Page
from tests.pages.announcement_page import AnnouncementPage


@pytest.mark.admin
def test_delete_announcement(admin_page: Page):
    """Announcement – admin deletes the first announcement."""
    ann = AnnouncementPage(admin_page)
    ann.navigate_admin()
    ann.delete_first_announcement()
