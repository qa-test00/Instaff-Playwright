import pytest
from playwright.sync_api import Page, expect
from tests.pages.announcement_page import AnnouncementPage


@pytest.mark.employee
def test_view_announcement(employee_page: Page):
    """Announcement – employee can see the announcements section after login."""
    ann = AnnouncementPage(employee_page)

    # Dashboard landing page should show at least one announcement card
    expect(employee_page.locator(".well > div > .col-md-12").first).to_be_visible()

    ann.navigate_employee()
    expect(
        employee_page.get_by_role("heading", name=" Current Announcements").first
    ).to_be_visible()
