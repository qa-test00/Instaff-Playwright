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
        
        # Monitor console errors
        page.on("console", lambda msg: print(f"Console: {msg.type}: {msg.text}"))
        page.on("pageerror", lambda error: print(f"Page error: {error}"))

        # Log in
        page.goto("https://marben.staging.instaff.org/login?next=%2F")
        page.get_by_role("textbox", name="Enter your email address").click()
        page.get_by_role("textbox", name="Enter your email address").fill("marben@hutility.com")
        page.get_by_role("textbox", name="Enter your password").fill("Temp1234!!")
        page.get_by_role("button", name="Log In").click()

        # Navigate to Upload -> Normal PS
        page.get_by_role("link", name="Upload Pay Documents").click()
        page.wait_for_load_state("networkidle")
        
        # Fill form with proper waits
        page.locator("#pdf_config_id").select_option("321")
        page.wait_for_timeout(2000)
        

        page.locator("#file").set_input_files("resources/SamplePaystubs.pdf")

        page.get_by_role("textbox", name="# Of Pay Documents In Batch").fill("10")
        page.wait_for_timeout(2000)

        page.evaluate("""
            document.getElementById('file')
                .dispatchEvent(new Event('change', { bubbles: true }));
            """)
        
        upload_btn = page.locator("#uploadBtn")
        expect(upload_btn).to_be_enabled()

        with page.expect_response(lambda r: "upload" in r.url):
            upload_btn.click()
        #page.wait_for_function("() => document.querySelector('#file').files.length > 0")

        
        # Wait for upload processingS
        page.wait_for_load_state("networkidle")
        
        # Rest of your test...
        locator = page.locator('span.label.label-success', has_text='Ready For Preview')
        locator.wait_for(state='visible')
        page.locator("#dt_basic > tbody > tr > td:nth-child(8) > a").click()

        page.wait_for_timeout(5000)
        expect(page.get_by_text("10 Parsed Documents Search: #")).to_be_visible()
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.get_by_role("button", name="Accept Parsed Document").click()
        expect(page.locator("#smallbox1")).to_be_visible()

        context.close()
        browser.close()
