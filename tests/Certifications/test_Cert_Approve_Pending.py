import pytest
from playwright.sync_api import Page
from tests.pages.certifications_page import CertificationsPage


@pytest.mark.admin
def test_cert_approve_pending(admin_page: Page):
    """Certifications – admin approves a pending employee certification record."""
    cert = CertificationsPage(admin_page)

    # Step 3: Go to /admin/certifications
    cert.navigate_admin()

    # Step 4: Click "Pending Employee Records" tab
    cert.click_pending_employee_records_tab()

    # Step 5: Check the checkbox for Auto Employee's pending certification
    cert.check_pending_record_for_employee("Auto Employee")

    # Step 6: Click "Approve Selected" button
    cert.click_approve_selected()

    # Step 7: Click "Approve" on the modal
    cert.confirm_approve()
