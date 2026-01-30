from playwright.sync_api import Playwright, sync_playwright, expect
import os

IS_CI = os.getenv("CI") is not None

def test_to_create_req():
    """
    Test for Time Off - Create Request.
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

        # Navigate to Time Off -> Create Request    
        page.get_by_role("link", name=" Time Off Request").click()
        page.get_by_role("button", name="Create New Request").click(delay=3000)
        # Fill in request details
        page.locator("#timeoffcomments").click(delay=3000)
        page.locator("#timeoffcomments").fill("Regression Test")
        page.get_by_role("button", name="Add").click(delay=3000)
        # Verify success message
        expect(page.locator("#smallbox1")).to_be_visible() # Verify success message

        # ---------------------
        context.close()
        browser.close()

