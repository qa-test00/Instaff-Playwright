from playwright.sync_api import Playwright, sync_playwright, expect
import os

IS_CI = os.getenv("CI") is not None

def test_tt_data_entry():
    """
    Test for Time Tracking - Regular Data Entry.
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
        page.get_by_role("link", name=" Time Tracking").click()

        # Fill in data entry details
        page.locator("#hours").click(delay=3000)
        page.locator("#hours").fill("8")
        page.get_by_role("textbox", name="Select a date").click(delay=3000)
        page.get_by_role("columnheader", name=" Next Month").click(delay=3000)
        page.get_by_role("cell", name="10").first.click(delay=3000)
       
        page.locator("#comments").click(delay=3000)


        page.locator("#comments").fill("Reg Test")
        page.get_by_role("button", name="Add Selected").click(delay=3000)
        expect(page.locator("#smallbox1")).to_be_visible() # Verify success message

        page.wait_for_load_state("networkidle")
        page.get_by_role("link", name="Unsubmitted Entries").click(delay=3000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)
        
        entryDate = page.locator("#dt_basic_unsubmitted > tbody > tr:nth-child(1) > td:nth-child(1)").text_content()
        print(entryDate.strip())

        page.locator("#checkAllUnsubmitted").uncheck()

        rowName = f"{entryDate} Reg Test 8.00"
        page.get_by_role("row", name=rowName).locator("#unsubmitted_entry_checkbox").check()
        page.get_by_role("checkbox", name="I Certify That All Above Time").check()
        page.get_by_role("button", name="Submit Selected Entries To").click(delay=3000)
        expect(page.locator("#smallbox1")).to_be_visible() # Verify success message

        # ---------------------
        context.close()
        browser.close()
