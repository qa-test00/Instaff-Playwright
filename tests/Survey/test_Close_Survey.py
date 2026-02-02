from socket import timeout
from playwright.sync_api import Playwright, sync_playwright, expect
import os

IS_CI = os.getenv("CI") is not None

def test_view_analytics_responses():
    """
    Test for Survey - View Analytics Responses.
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
        page.get_by_role("textbox", name="Enter your email address").fill("marben@hutility.com")
        page.get_by_role("textbox", name="Enter your email address").press("Tab")
        page.get_by_role("textbox", name="Enter your password").fill("Temp1234!!")
        page.get_by_role("button", name="Log In").click()

        # Navigate to Survey -> Close Survey
        page.get_by_role("link", name="Survey Management").click(delay=3000)
        page.wait_for_timeout(5000)
        page.get_by_role("row", name="Regression Testing  Always").get_by_role("button").nth(2).click(delay=3000)
        page.once("dialog", lambda dialog: dialog.accept())
        page.get_by_role("button", name=" Close Survey").click(delay=3000)
        page.once("dialog", lambda dialog: dialog.accept())
        expect(page.get_by_text("\"Regression Testing\" has been")).to_be_visible()

        # ---------------------
        context.close()
        browser.close()

