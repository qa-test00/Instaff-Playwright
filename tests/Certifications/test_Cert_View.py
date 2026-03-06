import pytest
from playwright.sync_api import Page
from tests.pages.certifications_page import CertificationsPage


@pytest.mark.employee
def test_cert_view(employee_page: Page):
    """Certifications – employee views an uploaded certificate."""
    cert = CertificationsPage(employee_page)

    # Step 2: Go to Certifications page
    cert.navigate()

    # Step 3: Click the "View" button for the uploaded certification
    cert.click_view_button("Reg Test")

    # Step 4: Verify the PDF viewer modal is displayed with the correct file
    cert.verify_pdf_viewer_displayed("2025 Security Awareness.pdf")
