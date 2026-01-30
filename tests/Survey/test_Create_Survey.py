from socket import timeout
from playwright.sync_api import Playwright, sync_playwright, expect
import os

IS_CI = os.getenv("CI") is not None

def test_create_survey():
    """
    Test for Survey - Create Survey.
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

        # Navigate to Survey -> Create Survey
        page.get_by_role("link", name="Survey Management").click(delay=3000)
        page.get_by_role("link", name=" Create New Survey").click()
        page.get_by_role("textbox", name="Survey Title").click(delay=3000)
        page.get_by_role("textbox", name="Survey Title").fill("Regression Testing")
        page.get_by_role("button", name=" Add Question").click(delay=3000)
        page.get_by_role("textbox", name="Question Text").fill("Question #1")
        page.get_by_role("checkbox", name=" Required Question").click(delay=3000)


        page.get_by_role("button", name=" Add Question").click(delay=3000)
        page.locator("#question_text_new_2").fill("Question #2")
        page.locator("#question_type_new_2").select_option("multiple_choice")
        #expect(page.get_by_role("button", name=" Add Option")).to_be_visible(timeout=5000)
        page.get_by_role("textbox", name="Enter option text").first.click(delay=3000)
        page.get_by_role("textbox", name="Enter option text").first.fill("A")
        page.get_by_role("textbox", name="Enter option text").nth(1).click()
        page.get_by_role("textbox", name="Enter option text").nth(1).fill("B")
        page.get_by_role("button", name=" Add Option").click(delay=3000)
        page.get_by_role("textbox", name="Enter option text").nth(2).click()
        page.get_by_role("textbox", name="Enter option text").nth(2).fill("C")
        page.get_by_role("checkbox", name="Enable additional suggestions").check()


        page.get_by_role("button", name=" Add Question").click(delay=3000)
        page.locator("#question_text_new_3").fill("Question #3")
        page.locator("#question_type_new_3").select_option("multiple_choice_multi")
        page.get_by_role("textbox", name="Enter option text").nth(3).click()
        page.get_by_role("textbox", name="Enter option text").nth(3).fill("1")
        page.get_by_role("textbox", name="Enter option text").nth(3).press("Tab")
        page.get_by_role("textbox", name="Enter option text").nth(4).click()
        page.get_by_role("textbox", name="Enter option text").nth(4).fill("2")
        page.locator("#options_editor_new_3").get_by_role("button", name=" Add Option").click(delay=3000)
        page.get_by_role("textbox", name="Enter option text").nth(5).click()
        page.get_by_role("textbox", name="Enter option text").nth(5).fill("3")
        page.locator("#is_required_new_3").check()


        page.get_by_role("button", name=" Add Question").click(delay=3000)
        page.locator("#question_text_new_4").fill("Question #4")
        page.locator("#question_type_new_4").select_option("ranking")
        #page.locator("#options_editor_new_4").get_by_role("button", name=" Add Option").click(delay=3000)
        page.locator("input[name=\"questions[new_4][options][]\"]").first.click()
        page.locator("input[name=\"questions[new_4][options][]\"]").first.fill("X")
        page.locator("input[name=\"questions[new_4][options][]\"]").nth(1).click()
        page.locator("input[name=\"questions[new_4][options][]\"]").nth(1).fill("Y")
        page.locator("#options_editor_new_4").get_by_role("button", name=" Add Option").click(delay=3000)
        page.locator("input[name=\"questions[new_4][options][]\"]").nth(2).click()
        page.locator("input[name=\"questions[new_4][options][]\"]").nth(2).fill("Z")
        page.get_by_role("spinbutton", name="Number of items to rank").click(delay=3000)
        page.get_by_role("spinbutton", name="Number of items to rank").fill("3")
        page.get_by_role("checkbox", name="Enable \"Other\" option in").check()
        page.locator("#allow_suggestions_new_4").check()
        page.locator("#is_required_new_4").check()


        page.get_by_role("button", name=" Create Survey Draft").click(delay=3000)
        #page.once("dialog", lambda dialog: dialog.dismiss())
        #page.get_by_role("button", name="  Publish Survey Now").click(delay=3000)
        page.locator("#content > div > div > div > div.mt-5.pt-5 > div > div.card-body.px-5.py-4 > div.text-center.pb-2 > form > button").click(delay=3000)
        page.locator("#content > div > div > div > div.mt-5.pt-5 > div > div.card-body.px-5.py-4 > div.text-center.pb-2 > form > button").click(delay=3000)
        page.wait_for_timeout(3000)
        page.keyboard.press("Enter")
        expect(page.locator("#content > div > div > div > div.alert.alert-success")).to_be_visible(timeout=5000)

        # ---------------------
        context.close()
        browser.close()

