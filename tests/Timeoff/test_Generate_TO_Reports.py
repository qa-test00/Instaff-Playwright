import pytest
from playwright.sync_api import Page, expect
from tests.pages.time_off_page import TimeOffPage


@pytest.mark.admin
def test_generate_to_reports(admin_page: Page):
    """Time Off – admin generates a report for a specific employee."""
    to = TimeOffPage(admin_page)
    to.navigate_to_reports()
    to.generate_report(employee_search="auto employee")
    expect(admin_page.get_by_role("gridcell", name="AUTOEMP").nth(0)).to_be_visible()
