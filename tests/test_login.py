import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage

def test_verify_login_page_loads_successfully(page: Page, app_url: str) -> None:
    login_page = LoginPage(page, app_url)
    
    login_page.navigate()
    login_page.verify_login_page_loaded()

def test_verify_succcessful_login(page: Page, app_url: str) -> None:
    login_page = LoginPage(page, app_url)
    
    login_page.navigate()
    login_page.login("admin", "gausslabs")
    login_page.verify_login_successful()

def test_verify_unsuccessful_login(page: Page, app_url: str) -> None:
    login_page = LoginPage(page, app_url)
    
    login_page.navigate()
    login_page.login("invalid_user", "invalid_password")
    login_page.verify_invalid_login_message()
    login_page.verify_still_on_login_page()

@pytest.mark.parametrize("username, password, expected_error",
                         [
                            pytest.param("", "", ["Username is required.", "Password you entered is invalid."], id="empty_both_fields"),
                            pytest.param("admin", "", ["Password you entered is invalid."], id="empty_password"),
                            pytest.param("", "gausslabs", ["Username is required."], id="empty_username"),
                        ],
                        )
def test_verify_login_errors(page: Page, app_url: str, username: str, password: str, expected_error: list) -> None:
    login_page = LoginPage(page, app_url)

    login_page.navigate()
    login_page.login(username, password)

    for error in expected_error:
        login_page.verify_validation_message(error)

    login_page.verify_still_on_login_page()
