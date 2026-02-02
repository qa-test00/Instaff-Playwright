from playwright.sync_api import Playwright, sync_playwright, expect
import os

IS_CI = os.getenv("CI") is not None

def test_manager_view_files():
    """
    Test for Manager - View Files.
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

        # Navigate to Manager -> My Employees
        page.get_by_role("link", name=" Manager ").click()
        page.get_by_role("link", name="My Employees").click()
        page.get_by_role("row", name="100050 John Rees Haley III").get_by_role("button").click()

        # Navigate to Manager -> See Paystubs
        page.get_by_role("link", name="See Paystubs").click()
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="View").click()
        page.wait_for_timeout(5000)
        expect(page.locator("#pdfViewer div").nth(1)).to_be_visible()

        # Navigate to Manager -> See Tax Forms
        page.goto("https://marben.staging.instaff.org/manager/employees")
        page.get_by_role("row", name="100050 John Rees Haley III").get_by_role("button").click()
        page.get_by_role("link", name="See Tax Forms").click()
        expect(page.locator("h2")).to_be_visible()

        # ---------------------
        context.close()
        browser.close()
