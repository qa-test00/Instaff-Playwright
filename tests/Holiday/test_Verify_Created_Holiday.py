import enum
from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime
import os
import json

with open("shared_data.json", "r") as f:
    holidays = json.load(f)

IS_CI = os.getenv("CI") is not None

def test_create_holiday():
    """
    Test for Holiday - Create Holiday.
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


        page.get_by_role("link", name=" Holidays").click()
        page.wait_for_load_state("networkidle")

        holiday_elements = page.locator("#content > div > div > div:nth-child(3) > div > ul > li")
        count = holiday_elements.count()

        assert count == len(holidays), f"Expected {len(holidays)} holidays, found {count}"

        for i, holiday in enumerate(holidays):
            expected_line = f"{holiday['holiday_Name']}, {holiday['date']}"
            actual_line = holiday_elements.nth(i).inner_text().strip()

            assert actual_line == expected_line, f"Expected '{expected_line}' but got '{actual_line}'"
            print(f"✅ Verified: {actual_line}")

        # ---------------------
        context.close()
        browser.close()
