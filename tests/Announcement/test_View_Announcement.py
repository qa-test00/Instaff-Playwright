from playwright.sync_api import Playwright, sync_playwright, expect
import os

#IS_CI = os.getenv("CI") is not None

def test_upload_normal_ps():
    """
    Test for Upload - Normal PS.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', 
            headless=False
        )
        context = browser.new_context()
        page = context.new_page()

        #Login
        page.goto("https://marben.staging.instaff.org/login?next=%2F")
        page.get_by_role("textbox", name="Enter your email address").click()
        page.get_by_role("textbox", name="Enter your email address").fill("marben+employee1@hutility.com")
        page.get_by_role("textbox", name="Enter your email address").press("Tab")
        page.get_by_role("textbox", name="Enter your password").fill("Temp1234!!")
        page.get_by_role("button", name="Log In").click()

        page.wait_for_load_state("networkidle")
        expect(page.locator(".well > div > .col-md-12").first).to_be_visible()
        page.get_by_role("link", name=" Announcements").click()
        page.wait_for_load_state("networkidle")
        expect(page.get_by_role("heading", name=" Current Announcements")).to_be_visible()

        # ---------------------
        context.close()
        browser.close()

