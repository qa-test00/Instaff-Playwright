import pytest
from playwright.sync_api import Page, expect
from tests.pages.upload_docs_page import UploadDocsPage


@pytest.mark.admin
def test_upload_scheduled_ps(admin_page: Page):
    """Upload – admin uploads a scheduled paystub batch with a future release date."""
    upload = UploadDocsPage(admin_page)
    upload.navigate()
    upload.upload_scheduled_paystub(
        config_id="321",
        file_path="resources/SamplePaystubs.pdf",
        doc_count="10",
        release_date="04/01/2026",
    )
    upload.accept_parsed_documents()
    expect(admin_page.get_by_text("10 Parsed Documents Search: #")).to_be_visible()
