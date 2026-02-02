from playwright.sync_api import Playwright, sync_playwright, expect
import os

IS_CI = os.getenv("CI") is not None

def test_approve_to_req_manager():
    """
    Test for Time Off - Manager Approval.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            permissions=["geolocation"],
            geolocation={"latitude": 37.7749, "longitude": -122.4194},
        )
        page = context.new_page()

        #Login
        page.goto("https://marben.staging.instaff.org/login?next=%2F")
        page.get_by_role("textbox", name="Enter your email address").click()
        page.get_by_role("textbox", name="Enter your email address").fill("marben@hutility.com")
        page.get_by_role("textbox", name="Enter your email address").press("Tab")
        page.get_by_role("textbox", name="Enter your password").fill("Temp1234!!")
        page.get_by_role("button", name="Log In").click()

        page.get_by_role("link", name="Holidays", exact=True).click()
        page.wait_for_load_state("networkidle")
        page.once("dialog", lambda dialog: dialog.accept())
        page.get_by_role("button", name="Delete").click()
        expect(page.locator("#smallbox1")).to_be_visible()

        # ---------------------
        context.close()
        browser.close()
