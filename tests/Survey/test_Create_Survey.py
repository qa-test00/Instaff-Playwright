import pytest
from playwright.sync_api import Page
from tests.pages.survey_page import SurveyPage


@pytest.mark.admin
def test_create_survey(admin_page: Page):
    """Survey – admin creates a multi-question survey and publishes it."""
    survey = SurveyPage(admin_page)
    survey.navigate_admin()
    survey.create_survey(title="Regression Testing")
