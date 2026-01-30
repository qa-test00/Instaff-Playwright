from playwright.sync_api import Playwright, sync_playwright, expect
import os

IS_CI = os.getenv("CI") is not None

def test_deny_to_req_admin():
    """
    Test for Time Off - Admin Deny.
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

        # Navigate to Time Off -> Admin
        page.get_by_role("link", name="Time Off Requests ").click()
        page.get_by_role("link", name="Time Off Manager").click()

        # Click the first "Cancel Request" and confirm, then verify that *that row's*
        # cancel button disappears (there may be other cancel buttons on the page).
        cancel_in_row = page.get_by_role("button", name="Cancel Request").first
        row = cancel_in_row.locator("xpath=ancestor::tr")

        # Some pages use an in-page modal, others use a browser dialog.
        page.once("dialog", lambda dialog: dialog.accept())
        cancel_in_row.click()

        # If an in-page confirmation modal appears, confirm it.
        for confirm in (
            page.get_by_role("button", name="Ok", exact=True),
            page.get_by_role("button", name="OK", exact=True),
            page.get_by_role("button", name="Yes", exact=True),
            page.get_by_role("button", name="Confirm", exact=True),
            page.get_by_role("button", name="Cancel Request", exact=True),
        ):
            try:
                confirm.click(timeout=5000)
                break
            except Exception:
                pass

        page.wait_for_load_state("networkidle")

        expect(row.get_by_role("button", name="Cancel Request")).to_be_hidden(timeout=15000)

        # ---------------------
        context.close()
        browser.close()
