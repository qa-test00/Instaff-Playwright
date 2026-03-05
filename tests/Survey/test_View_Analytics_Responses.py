import pytest
from playwright.sync_api import Page, expect
from tests.pages.survey_page import SurveyPage


@pytest.mark.admin
def test_view_analytics_responses(admin_page: Page):
    """Survey – admin views individual responses and analytics for the survey."""
    survey = SurveyPage(admin_page)
    survey.navigate_admin()
    survey.open_survey_details(survey_title="Regression Testing")
    survey.view_responses()

    expect(
        admin_page.get_by_role("heading", name=" Individual Responses (1)")
    ).to_be_visible()

    admin_page.get_by_text("Auto Employee (marben+").click()
    expect(admin_page.get_by_role("link", name=" View Analytics")).to_be_visible()

    survey.view_analytics()

    # Verify each question's response in the analytics view
    admin_page.get_by_text("Question 1: Question #").click()
    expect(admin_page.get_by_text("Test", exact=True)).to_be_visible()

    admin_page.get_by_text("Question 2: Question #").click()
    expect(admin_page.get_by_text("B 1 (100.0%)")).to_be_visible()

    admin_page.get_by_text("Question 3: Question #").click()
    expect(admin_page.get_by_text("2 1 (100.0%)")).to_be_visible()
    expect(admin_page.get_by_text("3 1 (100.0%)")).to_be_visible()

    admin_page.get_by_text("Question 4: Question #").click()
    expect(
        admin_page.get_by_text(
            "Total Responses: 1 (100.0% response rate) Ranking Results 1 Total Responses 3"
        )
    ).to_be_visible()
