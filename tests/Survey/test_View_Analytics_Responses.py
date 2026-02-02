from socket import timeout
from playwright.sync_api import Playwright, sync_playwright, expect
import os

IS_CI = os.getenv("CI") is not None

def test_view_analytics_responses():
    """
    Test for Survey - View Analytics Responses.
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

        # Navigate to Survey -> View Analytics Responses
        page.get_by_role("link", name="Survey Management").click(delay=3000)
        page.get_by_role("row", name="Regression Testing  Always").get_by_role("button").nth(1).click(delay=3000)
        page.get_by_role("link", name=" View Responses").click(delay=3000)
        expect(page.get_by_role("heading", name=" Individual Responses (1)")).to_be_visible()
        page.get_by_text("Auto Employee (marben+").click()
        expect(page.get_by_role("link", name=" View Analytics")).to_be_visible()

        # Navigate to Survey -> View Analytics
        page.get_by_role("link", name=" View Analytics").click()
        page.get_by_text("Question 1: Question #").click()
        expect(page.get_by_text("Test", exact=True)).to_be_visible()
        page.get_by_text("Question 2: Question #").click()
        expect(page.get_by_text("B 1 (100.0%)")).to_be_visible()
        page.get_by_text("Question 3: Question #").click()
        expect(page.get_by_text("2 1 (100.0%)")).to_be_visible()
        expect(page.get_by_text("3 1 (100.0%)")).to_be_visible()
        page.get_by_text("Question 4: Question #").click()
        expect(page.get_by_text("Total Responses: 1 (100.0% response rate) Ranking Results 1 Total Responses 3")).to_be_visible() 

        # ---------------------
        context.close()
        browser.close()
