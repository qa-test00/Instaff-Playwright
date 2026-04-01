import pytest
from playwright.sync_api import Page
from tests.pages.certifications_page import CertificationsPage
import config


@pytest.mark.admin
def test_cert_delete_record(admin_page: Page):
    """Certifications – admin deletes an employee certification record."""
    cert = CertificationsPage(admin_page)

    # Step 2: Go to /admin/certifications
    cert.navigate_admin()

    # Step 3: Click "Details" for "With Custom Fields"
    cert.click_details_for_cert("With Custom Fields")

    # Step 4: Click "Employee Records" tab
    cert.click_employee_records_tab()

    # Step 5: Search for "Auto Employee"
    cert.search_employee_records("Auto Employee")

    # Step 6: Click "Edit" for Auto Employee
    cert.click_edit_for_employee("Auto Employee")

    # Step 7: Click "Delete Record?" button
    cert.click_delete_record_button()

    # Step 8: Enter admin password
    cert.enter_admin_password(config.ADMIN_PASSWORD)

    # Step 9: Click "Delete"
    cert.click_delete_confirm()

    # Step 10: Verify success notification
    cert.verify_delete_success()
