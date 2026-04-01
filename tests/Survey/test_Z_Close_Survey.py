import pytest
from playwright.sync_api import Page, expect
from tests.pages.survey_page import SurveyPage


@pytest.mark.admin
def test_close_survey(admin_page: Page):
    """Survey – admin closes the regression survey."""
    survey = SurveyPage(admin_page)
    survey.navigate_admin()
    survey.close_survey(survey_title="Regression Testing")
    expect(
        admin_page.get_by_text('"Regression Testing" has been')
    ).to_be_visible(timeout=15000)
