import pytest
from playwright.sync_api import Page
from tests.pages.manager_page import ManagerPage

EMPLOYEE_ROW = "100050 John Rees Haley III"


@pytest.mark.admin
def test_manager_view_files(admin_page: Page):
    """Manager – view an employee's paystubs and tax forms."""
    mgr = ManagerPage(admin_page)
    mgr.navigate_employees()
    mgr.view_paystubs(EMPLOYEE_ROW)
    mgr.view_tax_forms(EMPLOYEE_ROW)
