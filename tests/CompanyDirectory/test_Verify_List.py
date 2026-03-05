import pytest
from playwright.sync_api import Page, expect
from tests.pages.company_directory_page import CompanyDirectoryPage


@pytest.mark.admin
def test_verify_list(admin_page: Page):
    """Company Directory – verify the employee directory list is visible on pages 1 and 2."""
    cd = CompanyDirectoryPage(admin_page)
    cd.navigate()

    expect(admin_page.locator("#directory-list")).to_be_visible()

    admin_page.get_by_role("link", name="2", exact=True).click()
    expect(admin_page.locator("#directory-list")).to_be_visible()
