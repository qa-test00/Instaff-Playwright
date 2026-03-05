import pytest
from playwright.sync_api import Page
from tests.pages.survey_page import SurveyPage


@pytest.mark.employee
def test_respond_survey(employee_page: Page):
    """Survey – employee responds to the published regression survey."""
    survey = SurveyPage(employee_page)
    survey.navigate_employee()
    survey.respond_to_survey(survey_title="Regression Testing")
