"""
UploadDocsPage: actions for the Upload Pay Documents module.
"""
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage


class UploadDocsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate(self) -> None:
        self.page.get_by_role("link", name="Upload Pay Documents").click()
        self.wait_for_load()

    def upload_paystub(
        self, config_id: str, file_path: str, doc_count: str
    ) -> None:
        self.page.locator("#pdf_config_id").select_option(config_id)
        self.page.locator("#file").set_input_files(file_path)
        self.page.get_by_role("textbox", name="# Of Pay Documents In Batch").fill(
            doc_count
        )
        # Trigger the change event so the UI recognises the file selection
        self.page.evaluate(
            "document.getElementById('file').dispatchEvent(new Event('change', { bubbles: true }))"
        )
        upload_btn = self.page.locator("#uploadBtn")
        expect(upload_btn).to_be_enabled()
        with self.page.expect_response(lambda r: "upload" in r.url):
            upload_btn.click()
        self.wait_for_load()

    def accept_parsed_documents(self, expected_label: str = "Ready For Preview") -> None:
        ready_label = self.page.locator(
            "span.label.label-success", has_text=expected_label
        )
        ready_label.wait_for(state="visible", timeout=30000)
        self.page.locator("#dt_basic > tbody > tr > td:nth-child(8) > a").click()
        # Allow time for the preview panel to render
        self.page.wait_for_timeout(5000)
        self.page.once("dialog", lambda dialog: dialog.dismiss())
        self.page.get_by_role("button", name="Accept Parsed Document").click()
        self.expect_success_toast()
