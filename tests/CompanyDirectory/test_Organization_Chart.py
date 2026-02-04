from playwright.sync_api import Playwright, sync_playwright, expect
import os

#IS_CI = os.getenv("CI") is not None

def test_organization_chart():
    """
    Test for Company Directory - Verify Org Chart.
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
        page.get_by_role("textbox", name="Enter your email address").click()
        page.get_by_role("textbox", name="Enter your email address").fill("marben@hutility.com")
        page.get_by_role("textbox", name="Enter your email address").press("Tab")
        page.get_by_role("textbox", name="Enter your password").fill("Temp1234!!")
        page.get_by_role("button", name="Log In").click()
        
        page.get_by_role("link", name=" Company Directory").click()
        page.wait_for_load_state("networkidle")
        page.get_by_role("link", name=" Organization Chart").click()
        page.wait_for_load_state("networkidle")

        expect(page.locator(".org-chart-header")).to_be_visible()
        page.get_by_role("button", name=" Add Position").click()
        page.wait_for_load_state("networkidle")

        expect(page.get_by_role("heading", name="Add New Position")).to_be_visible()
        page.get_by_role("textbox", name="Position Title *").click()
        page.get_by_role("textbox", name="Position Title *").fill("Reg Test Title")
        page.get_by_role("textbox", name="Description").click()
        page.get_by_role("textbox", name="Description").fill("Regression Test")
        page.get_by_role("dialog", name="Add New Position").get_by_label("Department").select_option("79")
        page.get_by_label("Reports To").select_option("67")
        page.get_by_role("button", name=" Create Position").click()
        page.wait_for_load_state("networkidle")
        expect(page.locator("div").filter(has_text="✅ Position created").nth(1)).to_be_visible()
        page.wait_for_load_state("networkidle")
        expect(page.get_by_text("Vacant Position Reg Test")).to_be_visible()
        page.get_by_role("button", name=" Edit").nth(4).click()
        page.wait_for_load_state("networkidle")
        page.once("dialog", lambda dialog: dialog.accept())
        page.get_by_role("button", name=" Delete Position").click()

        # ---------------------
        context.close()
        browser.close()
