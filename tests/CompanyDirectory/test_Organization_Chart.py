import pytest
from playwright.sync_api import Page, expect
from tests.pages.company_directory_page import CompanyDirectoryPage


@pytest.mark.admin
def test_organization_chart(admin_page: Page):
    """Company Directory – add a new org-chart position then delete it."""
    cd = CompanyDirectoryPage(admin_page)
    cd.navigate()
    cd.navigate_org_chart()

    expect(admin_page.locator(".org-chart-header")).to_be_visible()

    cd.add_position(
        title="Reg Test Title",
        description="Regression Test",
        department_option="79",
        reports_to_option="67",
    )
    expect(admin_page.get_by_text("Vacant Position Reg Test")).to_be_visible()

    cd.delete_position(nth=4)
