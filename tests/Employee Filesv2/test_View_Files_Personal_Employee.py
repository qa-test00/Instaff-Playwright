import pytest
from playwright.sync_api import Page
from tests.pages.employee_files_page import EmployeeFilesPage


@pytest.mark.employee
def test_view_files_personal_employee(employee_page: Page):
    """Employee – view files in Private, Uncategorized, and Personal AUTOEMP folders."""
    files = EmployeeFilesPage(employee_page)

    # Step 3: Go to Files page
    files.navigate()

    # Step 4-6: View a file inside "Private Files"
    files.view_folder("Private Files")
    files.view_first_file()
    files.verify_file_opened()

    # Step 7: Go back to Files page
    files.go_back_to_files()

    # Step 8-10: View a file inside "Uncategorized Files"
    files.view_folder("Uncategorized Files")
    files.view_first_file()
    files.verify_file_opened()

    # Step 11: Go back to Files page
    files.go_back_to_files()

    # Step 12-15: Navigate into "Personal AUTOEMP Folder" → "Subfolder" → view a file
    files.view_folder("Personal AUTOEMP Folder")
    files.view_folder("Subfolder")
    files.view_first_file()
    files.verify_file_opened()

    # Step 16: Go back to Files page
    files.go_back_to_files()
