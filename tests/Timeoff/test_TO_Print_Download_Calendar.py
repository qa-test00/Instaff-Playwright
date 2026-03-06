import pytest
from playwright.sync_api import Page
from tests.pages.time_off_page import TimeOffPage


@pytest.mark.admin
def test_to_print_download_calendar(admin_page: Page):
    """Time Off – admin prints calendar to PDF and downloads iCal file."""
    to = TimeOffPage(admin_page)
    to.navigate_to_admin_timeoff()

    pdf_filename = to.print_calendar_to_pdf()
    assert pdf_filename.lower().endswith(".pdf"), f"PDF download failed: {pdf_filename}"

    ical_filename = to.download_calendar_ical()
    assert ical_filename.lower().endswith(".ics"), f"iCal download failed: {ical_filename}"
