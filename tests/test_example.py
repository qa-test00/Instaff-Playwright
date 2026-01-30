from playwright.sync_api import sync_playwright, expect


def test_example():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://marben.staging.instaff.org/login?next=%2F")
        page.get_by_role("textbox", name="  Please enter your email").click()
        page.get_by_role("textbox", name="  Please enter your email").fill("marben@hutility.com")
        page.get_by_role("textbox", name="  Enter your password").click()
        page.get_by_role("textbox", name="  Enter your password").fill("Temp1234!!")
        page.get_by_role("button", name="Log In").click()
        page.get_by_role("button", name="×").click()
        expect(page.get_by_role("heading", name="Hi, Marben Dimson''")).to_be_visible()

        context.close()
        browser.close()
