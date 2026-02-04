from playwright.sync_api import Playwright, sync_playwright, expect
import os

#IS_CI = os.getenv("CI") is not None

def test_verify_list():
    """
    Test for Company Directory - Verify Directory List.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', 
            headless=False
        )
        context = browser.new_context()
        page = context.new_page()
            
        page.goto("https://marben.staging.instaff.org/login?next=%2F")
        page.get_by_role("textbox", name="Enter your email address").click()
        page.get_by_role("textbox", name="Enter your email address").click()
        page.get_by_role("textbox", name="Enter your email address").fill("marben@hutility.com")
        page.get_by_role("textbox", name="Enter your email address").press("Tab")
        page.get_by_role("textbox", name="Enter your password").fill("Temp1234!!")
        page.get_by_role("button", name="Log In").click()
        page.get_by_role("link", name=" Company Directory").click()

        #Verify Directory List on page 1
        expect(page.locator("#directory-list")).to_be_visible()

        #Verify Directory List on page 2
        page.get_by_role("link", name="2", exact=True).click()
        expect(page.locator("#directory-list")).to_be_visible()

        # ---------------------
        context.close()
        browser.close()

