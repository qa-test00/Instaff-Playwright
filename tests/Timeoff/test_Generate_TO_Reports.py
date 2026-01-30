from playwright.sync_api import Playwright, sync_playwright, expect
import os
import re

IS_CI = os.getenv("CI") is not None

def test_generate_to_reports():
    """
    Test for Time Off - Generate Reports.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            permissions=["geolocation"],
            geolocation={"latitude": 37.7749, "longitude": -122.4194},
        )

        # Log in
        page = context.new_page()
        page.goto("https://marben.staging.instaff.org/login?next=%2F")
        page.get_by_role("textbox", name="Enter your email address").click()
        page.get_by_role("textbox", name="Enter your email address").fill("marben@hutility.com")
        page.get_by_role("textbox", name="Enter your email address").press("Tab")
        page.get_by_role("textbox", name="Enter your password").fill("Temp1234!!")
        page.get_by_role("button", name="Log In").click()

        # Navigate to Time Off -> Reports
        page.get_by_role("link", name="Time Off Requests ").click()
        page.get_by_role("link", name="Reports").click()
        page.locator("div").filter(has_text=re.compile(r"^All$")).first.click(delay=3000)
        # Fill in report details
        page.locator("#employeeid-selectized").fill("auto employee")
        page.locator("#employeeid-selectized").press("Enter")
        page.get_by_role("button", name="Build Report").click()
        expect(page.get_by_role("gridcell", name="AUTOEMP").nth(1)).to_be_visible() # Verify report generated

        # ---------------------
        context.close()
        browser.close()

