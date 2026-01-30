from playwright.sync_api import sync_playwright, expect
import os

IS_CI = os.getenv("CI") is not None

def test_tt_tbt_entry():
    """
    Test for Time Tracking - Track By Timer.
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
        page.get_by_role("textbox", name="Enter your email address").fill(
            "marben+employee1@hutility.com"
        )
        page.get_by_role("textbox", name="Enter your email address").press("Tab")
        page.get_by_role("textbox", name="Enter your password").fill("Temp1234!!")
        page.get_by_role("button", name="Log In").click()

        # Navigate to Time Tracking -> Track By Timer
        page.get_by_role("link", name=" Time Tracking").click()
        page.locator("a").filter(has_text="Track By Timer").click()

        # Fill in timer details and start timer
        page.locator("#jobnum_timer").click()
        page.locator("#jobnum_timer").fill("Job#1")
        page.locator("#comments_timer").click()
        page.locator("#comments_timer").fill("Regression Test")
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Start Timer").click(delay=5000)
        # Wait for Ok button to appear and click it
        ok_button = page.get_by_role("button", name="Ok", exact=True)
        ok_button.wait_for(state="visible", timeout=30000)
        ok_button.click()
        page.wait_for_timeout(2000)

        page.wait_for_timeout(10000)

        # Stop timer and verify
        expect(page.get_by_role("button", name="Stop Timer")).to_be_visible()
        page.get_by_role("button", name="Stop Timer").click(delay=5000)
        # Wait for Ok button to appear and click it
        ok_button = page.get_by_role("button", name="Ok", exact=True)
        ok_button.wait_for(state="visible", timeout=30000)
        ok_button.click()
        page.wait_for_timeout(2000)

        context.close()
        browser.close()
