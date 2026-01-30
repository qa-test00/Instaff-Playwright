from playwright.sync_api import Playwright, sync_playwright, expect
import os

IS_CI = os.getenv("CI") is not None

def test_approve_tt_entry_manager():
    """
    Test for Time Tracking - Manager Approval.
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

        # Navigate to Time Tracking -> Manager
        page.get_by_role("link", name=" Time Tracking").click()
        page.get_by_role("link", name=" Manager").click(delay=3000)
        #page.once("dialog", lambda dialog: dialog.dismiss(delay=3000))
        # Approve the first entry
        page.get_by_role("link", name="View").nth(1).click(delay=3000)
        for _ in range(3):
            page.keyboard.press("Escape")
            page.wait_for_timeout(2000)
        page.get_by_role("checkbox").nth(1).check()
        #page.once("dialog", lambda dialog: dialog.dismiss(delay=3000))
        page.get_by_role("button", name="Approve Selected Entries").click(delay=3000)
        for _ in range(3):
            page.keyboard.press("Escape")
            page.wait_for_timeout(2000)
        expect(page.locator("#smallbox1")).to_be_visible() # Verify success message

        # ---------------------
        context.close()
        browser.close()

