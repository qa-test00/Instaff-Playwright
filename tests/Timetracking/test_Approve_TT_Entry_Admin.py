from playwright.sync_api import Playwright, sync_playwright, expect
import os

IS_CI = os.getenv("CI") is not None

def test_approve_tt_entry_admin():
    """
    Test for Time Tracking - Admin Approval.
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

        # Navigate to Time Tracking -> Admin    
        page.locator("#left-panel").get_by_role("link", name="Time Tracking", exact=True).click()
        #page.get_by_role("link", name="Details").nth(2).click(delay=3000)
        page.goto("https://marben.staging.instaff.org/admin/timetracking/59")
        page.locator("input[name=\"entries_checkboxes_admin_awaiting_approval\"]").check()
        page.get_by_role("button", name="Approve Selected Entries").click(delay=3000)
        expect(page.locator("#smallbox1")).to_be_visible() # Verify success message

        # ---------------------
        context.close()
        browser.close()

