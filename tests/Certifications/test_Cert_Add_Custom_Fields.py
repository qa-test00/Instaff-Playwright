import pytest
from playwright.sync_api import Page
from tests.pages.certifications_page import CertificationsPage


@pytest.mark.employee
def test_cert_add_custom_fields(employee_page: Page):
    """Certifications – employee adds a new certificate with custom fields."""
    cert = CertificationsPage(employee_page)

    # Step 3: Go to Certifications page
    cert.navigate()

    # Step 4: Click "Add New Certificate"
    cert.open_add_certificate_modal()

    # Step 5: Select "With Custom Fields" in the Type dropdown
    cert.select_type_with_custom_fields()

    # Step 6: Verify "Required Fields" is a required field
    cert.verify_required_field_is_required()

    # Step 7: Verify "Non Required Fields" is not required
    cert.verify_non_required_field_is_not_required()

    # Steps 8-10: Fill form – required value, expiry date (10 days ahead), upload file
    cert.fill_add_certificate_form(
        required_value="Reg Test",
        file_path="resources/2025 Security Awareness.pdf",
        days_ahead=10,
    )

    # Step 12: Verify "Upload successful" notification
    cert.verify_upload_successful()

    # Step 13: Click "Pending" tab
    cert.click_pending_tab()

    # Step 14: Verify the uploaded certificate is visible in Pending
    cert.verify_certificate_in_pending("Reg Test")
