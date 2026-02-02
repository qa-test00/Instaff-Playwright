from playwright.sync_api._generated import ElementHandle


from socket import timeout
from playwright.sync_api import Playwright, sync_playwright, expect
import os

IS_CI = os.getenv("CI") is not None

def test_respond_survey():
    """
    Test for Survey - Respond to Survey.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            permissions=["geolocation"],
            geolocation={"latitude": 37.7749, "longitude": -122.4194},
        )
        page = context.new_page()
        
        # Log in
        page.goto("https://marben.staging.instaff.org/login?next=%2F")
        page.get_by_role("textbox", name="Enter your email address").click()
        page.get_by_role("textbox", name="Enter your email address").fill("marben+employee1@hutility.com")
        page.get_by_role("textbox", name="Enter your email address").press("Tab")
        page.get_by_role("textbox", name="Enter your password").fill("Temp1234!!")
        page.get_by_role("button", name="Log In").click()

        # Navigate to Survey -> Respond to Survey
        page.get_by_role("link", name=" Surveys").click()
        page.get_by_role("row", name="Regression Testing N/A").get_by_role("link").click()
        page.get_by_role("textbox", name="Enter your response here...").click()
        page.get_by_role("textbox", name="Enter your response here...").fill("Test")
        page.get_by_role("radio", name="B").check()
        #page.locator("textarea[name=\"suggestions_q516\"]").click()
        #page.locator("textarea[name=\"suggestions_q516\"]").fill("Testing")
        textareas = page.query_selector_all("textarea.form-control.mt-2")

        # Fill both
        for i, textarea in enumerate(textareas):
            textarea.fill(f"Test Input {i+1}")

        page.get_by_role("checkbox", name="2").check()
        page.get_by_role("checkbox", name="3").check()
        page.locator("select[data-rank=\"1\"]").select_option("X")
        page.locator("select[data-rank=\"2\"]").select_option("Z")
        page.locator("select[data-rank=\"3\"]").select_option("Y")
        #page.locator("textarea[name=\"suggestions_q518\"]").click()
        #page.locator("textarea[name=\"suggestions_q518\"]").fill("TEST")
        page.get_by_role("button", name=" Submit Survey").click()
        expect(page.get_by_text("Survey submitted successfully")).to_be_visible()

        # ---------------------
        context.close()
        browser.close()

