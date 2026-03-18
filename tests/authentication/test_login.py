import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.authentication
def test_verify_login_page_loads_successfully(login_page):
    """
    Verify that the login page loads successfully and that the main elements are visible.
    """
    login_page.navigate()
    login_page.verify_login_page_loaded()

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.authentication
def test_verify_successful_login(login_page, dashboard_page, env_config):
    """
    Verify that a user can log in successfully with valid credentials and is redirected to the dashboard page.
    """
    login_page.navigate()
    login_page.login(
        env_config["username"],
        env_config["password"]
    )
    dashboard_page.verify_dashboard_page_loaded()
    dashboard_page.wait_for_page_to_load()

@pytest.mark.regression
@pytest.mark.authentication
def test_verify_invalid_login(login_page, login_test_data):
    """
    Verify that an error message is shown when a user tries to log in with invalid credentials and that the user remains on the login page.
    """
    invalid_case = login_test_data["invalid_login_cases"][0]

    login_page.navigate()
    login_page.login(invalid_case["username"], invalid_case["password"])
    login_page.verify_invalid_login_message()
    login_page.verify_still_on_login_page()

@pytest.mark.regression
@pytest.mark.authentication
@pytest.mark.parametrize(
    "case_index,expected_check",
    [
        (2, "password"),
        (3, "username"),
    ]
)
def test_verify_login_with_partial_credentials(
    login_page,
    login_test_data,
    case_index,
    expected_check
):
    case = login_test_data["invalid_login_cases"][case_index]

    login_page.navigate()
    login_page.login(case["username"], case["password"])

    if expected_check == "password":
        login_page.verify_password_invalid_message()
    elif expected_check == "username":
        login_page.verify_username_required_message()

    login_page.verify_still_on_login_page()