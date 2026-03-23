from playwright.sync_api import expect, Page

from pages.base_page import BasePage

class LoginPage(BasePage):
    URL = "/login"

    def __init__(self, page: Page, app_url: str, env_name: str):
        super().__init__(page, app_url, env_name)

        self.username_input = page.get_by_label("Username")
        self.password_input = page.get_by_label("Password")
        self.login_button = page.get_by_role("button", name="Login")

        self.panoptes_logo = page.get_by_alt_text("panoptes")
        self.welcome_text = page.get_by_text("Welcome to")
        self.panoptes_text = page.get_by_text("Panoptes")
        self.subtitle_text = page.get_by_text("Let AI predict your process outcomes")
        self.robust_prediction_text = page.get_by_text("Robust Prediction")
        self.automatic_feature_selection_text = page.get_by_text("Automatic Feature Selection")
        self.flexible_customization_text = page.get_by_text("Flexible Customization")

        #Labels/placeholders
        self.login_heading = page.get_by_role("heading", name="Login")
        self.username_placeholder = page.get_by_placeholder("Gausslabs@gausslabs.ai")
        self.password_placeholder = page.get_by_placeholder("password")

        #Generic error message
        self.invalid_login_message = page.get_by_text("Invalid username or password.")
        self.username_required_message = page.get_by_text("Username is required.")
        self.password_invalid_message = page.get_by_text("Password you entered is invalid.")
    
    def navigate(self) -> None:
        super().navigate(self.URL)
        # self.page.goto(f"{self.app_url}/login")

    def verify_login_page_loaded(self) -> None:
        expect(self.panoptes_logo).to_be_visible()
        expect(self.welcome_text).to_be_visible()
        expect(self.panoptes_text).to_be_visible()
        expect(self.subtitle_text).to_be_visible()
        expect(self.robust_prediction_text).to_be_visible()
        expect(self.automatic_feature_selection_text).to_be_visible()
        expect(self.flexible_customization_text).to_be_visible()
        expect(self.login_heading).to_be_visible()
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.username_placeholder).to_be_visible()
        expect(self.password_placeholder).to_be_visible()
        expect(self.login_button).to_be_visible()

    def fill_username(self, username: str) -> None:
        self.username_input.fill(username)
    
    def fill_password(self, password: str) -> None:
        self.password_input.fill(password)
    
    def click_login(self) -> None:
        self.login_button.click()
    
    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def verify_login_successful(self) -> None:
        expect(self.page).not_to_have_url(f"{self.app_url}{self.URL}")

    def verify_invalid_login_message(self) -> None:
        expect(self.invalid_login_message.first).to_be_visible()

    def verify_validation_message(self, message: str) -> None:
        expect(self.page.get_by_text(message, exact=True)).to_be_visible()

    def verify_still_on_login_page(self) -> None:
        expect(self.page).to_have_url(f"{self.app_url}{self.URL}")
        expect(self.login_button).to_be_visible()

    def verify_username_required_message(self) -> None:
        expect(self.username_required_message).to_be_visible()

    def verify_password_invalid_message(self) -> None:
        expect(self.password_invalid_message).to_be_visible()