import pytest
from playwright.sync_api import Page
from tests.pages.paystubs_page import PaystubsPage


@pytest.mark.employee
def test_view_paystubs(john_page: Page):
    """Paystubs – employee (john) views a paystub file."""
    ps = PaystubsPage(john_page)

    # Step 3: Go to Paystubs page
    ps.navigate()

    # Step 4: Click "View" on the first file in the table
    ps.click_view_first()

    # Step 5: Verify that the View Paystubs PDF viewer is displayed
    ps.verify_pdf_viewer_displayed()
