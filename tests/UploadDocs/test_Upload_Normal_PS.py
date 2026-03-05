import pytest
from playwright.sync_api import Page, expect
from tests.pages.upload_docs_page import UploadDocsPage


@pytest.mark.admin
def test_upload_normal_ps(admin_page: Page):
    """Upload – admin uploads a normal paystub batch and accepts the parsed documents."""
    upload = UploadDocsPage(admin_page)
    upload.navigate()
    upload.upload_paystub(
        config_id="321",
        file_path="resources/SamplePaystubs.pdf",
        doc_count="10",
    )
    upload.accept_parsed_documents()
    expect(admin_page.get_by_text("10 Parsed Documents Search: #")).to_be_visible()
