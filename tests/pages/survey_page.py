"""
SurveyPage: actions for the Survey Management module.
"""
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage


class SurveyPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ------------------------------------------------------------------
    # Admin – Create survey
    # ------------------------------------------------------------------

    def navigate_admin(self) -> None:
        self.page.get_by_role("link", name="Survey Management").click()
        self.wait_for_load()

    def create_survey(self, title: str = "Regression Testing") -> None:
        self.page.get_by_role("link", name=" Create New Survey").click()
        # Click first to activate JS listeners on the title field
        self.page.get_by_role("textbox", name="Survey Title").click(delay=3000)
        self.page.get_by_role("textbox", name="Survey Title").fill(title)

        # Question 1 – short text, required
        self.page.get_by_role("button", name=" Add Question").click(delay=3000)
        self.page.get_by_role("textbox", name="Question Text").fill("Question #1")
        self.page.get_by_role("checkbox", name=" Required Question").click(delay=3000)

        # Question 2 – multiple choice (single answer)
        self.page.get_by_role("button", name=" Add Question").click(delay=3000)
        self.page.locator("#question_text_new_2").fill("Question #2")
        self.page.locator("#question_type_new_2").select_option("multiple_choice")
        self.page.get_by_role("textbox", name="Enter option text").first.click(delay=3000)
        self.page.get_by_role("textbox", name="Enter option text").first.fill("A")
        self.page.get_by_role("textbox", name="Enter option text").nth(1).click()
        self.page.get_by_role("textbox", name="Enter option text").nth(1).fill("B")
        self.page.get_by_role("button", name=" Add Option").click(delay=3000)
        self.page.get_by_role("textbox", name="Enter option text").nth(2).click()
        self.page.get_by_role("textbox", name="Enter option text").nth(2).fill("C")
        self.page.get_by_role("checkbox", name="Enable additional suggestions").check()

        # Question 3 – multiple choice (multi-select)
        self.page.get_by_role("button", name=" Add Question").click(delay=3000)
        self.page.locator("#question_text_new_3").fill("Question #3")
        self.page.locator("#question_type_new_3").select_option("multiple_choice_multi")
        self.page.get_by_role("textbox", name="Enter option text").nth(3).click()
        self.page.get_by_role("textbox", name="Enter option text").nth(3).fill("1")
        self.page.get_by_role("textbox", name="Enter option text").nth(3).press("Tab")
        self.page.get_by_role("textbox", name="Enter option text").nth(4).click()
        self.page.get_by_role("textbox", name="Enter option text").nth(4).fill("2")
        self.page.locator("#options_editor_new_3").get_by_role("button", name=" Add Option").click(delay=3000)
        self.page.get_by_role("textbox", name="Enter option text").nth(5).click()
        self.page.get_by_role("textbox", name="Enter option text").nth(5).fill("3")
        self.page.locator("#is_required_new_3").check()

        # Question 4 – ranking
        self.page.get_by_role("button", name=" Add Question").click(delay=3000)
        self.page.locator("#question_text_new_4").fill("Question #4")
        self.page.locator("#question_type_new_4").select_option("ranking")
        self.page.locator("input[name='questions[new_4][options][]']").first.click()
        self.page.locator("input[name='questions[new_4][options][]']").first.fill("X")
        self.page.locator("input[name='questions[new_4][options][]']").nth(1).click()
        self.page.locator("input[name='questions[new_4][options][]']").nth(1).fill("Y")
        self.page.wait_for_timeout(5000)
        self.page.locator("#options_editor_new_4").get_by_role("button", name=" Add Option").click(delay=5000)
        self.page.locator("input[name='questions[new_4][options][]']").nth(2).click()
        self.page.locator("input[name='questions[new_4][options][]']").nth(2).fill("Z")
        self.page.get_by_role("spinbutton", name="Number of items to rank").click(delay=3000)
        self.page.get_by_role("spinbutton", name="Number of items to rank").fill("3")
        self.page.get_by_role("checkbox", name='Enable "Other" option in').check()
        self.page.locator("#allow_suggestions_new_4").check()
        self.page.locator("#is_required_new_4").check()

        # Create draft then publish
        self.page.get_by_role("button", name=" Create Survey Draft").click(delay=3000)
        self.page.once("dialog", lambda dialog: dialog.dismiss())
        self.page.wait_for_timeout(5000)
        self.page.locator("form[method='post'] > .btn.btn-lg.btn-primary").click(delay=5000)
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.wait_for_timeout(5000)
        self.page.keyboard.press("Enter")
        expect(
            self.page.locator("#content > div > div > div > div.alert.alert-success")
        ).to_be_visible(timeout=15000)

    # ------------------------------------------------------------------
    # Employee – Respond to survey
    # ------------------------------------------------------------------

    def navigate_employee(self) -> None:
        self.page.get_by_role("link", name=" Surveys").click()
        self.wait_for_load()

    def respond_to_survey(self, survey_title: str = "Regression Testing") -> None:
        self.page.get_by_role("row", name=f"{survey_title} N/A").locator("a[href*='/surveys/take/']").click()
        self.wait_for_load()

        # Q1 – text answer
        self.page.get_by_role("textbox", name="Enter your response here...").fill("Test")

        # Q2 – single choice radio
        self.page.get_by_role("radio", name="B").check()

        # Fill all "other suggestion" text areas
        textareas = self.page.query_selector_all("textarea.form-control.mt-2")
        for i, textarea in enumerate(textareas):
            textarea.fill(f"Test Input {i + 1}")

        # Q3 – multi-select checkboxes
        self.page.get_by_role("checkbox", name="2").check()
        self.page.get_by_role("checkbox", name="3").check()

        # Q4 – ranking dropdowns
        self.page.locator("select[data-rank='1']").select_option("X")
        self.page.locator("select[data-rank='2']").select_option("Z")
        self.page.locator("select[data-rank='3']").select_option("Y")

        self.page.get_by_role("button", name=" Submit Survey").click()
        expect(self.page.get_by_text("Survey submitted successfully")).to_be_visible()

    # ------------------------------------------------------------------
    # Admin – View responses & analytics
    # ------------------------------------------------------------------

    def open_survey_details(self, survey_title: str = "Regression Testing") -> None:
        self.page.get_by_role("row", name=survey_title).get_by_role(
            "button"
        ).nth(1).click()
        self.wait_for_load()

    def view_responses(self) -> None:
        self.page.get_by_role("link", name=" View Responses").click()
        self.wait_for_load()

    def view_analytics(self) -> None:
        self.page.get_by_role("link", name=" View Analytics").click()
        self.wait_for_load()

    # ------------------------------------------------------------------
    # Admin – Close survey
    # ------------------------------------------------------------------

    def close_survey(self, survey_title: str = "Regression Testing") -> None:
        self.page.get_by_role("row", name=survey_title).get_by_role(
            "button"
        ).nth(2).click()
        self.wait_for_load()
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.get_by_role("button", name=" Close Survey").click()
        self.wait_for_load()
