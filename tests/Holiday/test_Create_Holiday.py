from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime
import os
import json

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


        page.get_by_role("link", name="Holidays", exact=True).click()
        page.wait_for_load_state("networkidle")

        page.get_by_text("Create New Holiday").click()
        page.locator("#holidayname").click()
        page.locator("#holidayname").fill("Regression Testing")
        page.locator("#description").click()

        holidays = []
        holiday_Name = page.locator("#holidayname").input_value().strip()
        start_Date = page.locator("#start-time").input_value().strip()

        date_td = datetime.strptime(start_Date, "%B %d, %Y")
        date_formatted = date_td.strftime("%B %d, %Y")

        holidays.append({
            "holiday_Name": holiday_Name,
            "date": date_formatted
        })

        with open("shared_data.json", "w") as f:
            json.dump(holidays, f, indent=2)

        page.locator("#description").fill("Reg Testing")
        page.locator("#notification").click()
        page.locator("#notification").fill("Reg automation testing")
        page.get_by_role("button", name="Submit").click()
        page.wait_for_load_state("networkidle")
        expect(page.locator("#smallbox1")).to_be_visible()

        # ---------------------
        context.close()
        browser.close()
