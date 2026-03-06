"""
PaystubsPage: actions for the Paystubs module (employee view).
"""
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage
import config


class PaystubsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate(self) -> None:
        self.page.locator("a[href='/paystubs']").first.click()
        self.wait_for_load()

    def click_view_first(self) -> None:
        self.page.get_by_role("button", name="View").first.click()
        self.page.wait_for_selector("#pdfViewer", state="visible")

    def verify_pdf_viewer_displayed(self) -> None:
        expect(self.page.locator("#pdfViewer")).to_be_visible(
            timeout=config.DEFAULT_TIMEOUT
        )
        expect(self.page.locator("#pdf_iframe")).to_be_visible(
            timeout=config.DEFAULT_TIMEOUT
        )
