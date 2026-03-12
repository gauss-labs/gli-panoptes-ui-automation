from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

class LeftNavigation:
    def __init__(self, page: Page) -> None:
        self.page = page

        self.nav_container: Locator = page.locator("nav")

        self.logo_link: Locator = page.locator("a[href='/']").first

        self.models_link: Locator = page.locator("nav a[href='/models']")
        self.create_model_link: Locator = page.locator("nav a[href='/create']")
        self.analytics_link: Locator = page.locator("nav a[href='/analytics']")
        self.batch_profile_link: Locator = page.locator("nav a[href='/batch-profiles']")

        self.language_button: Locator = page.get_by_role("button", name="Language")
        self.user_menu_button: Locator = page.get_by_role("button", name="admin")
        self.collapse_button: Locator = page.get_by_role("button", name="Collapse")

    def verify_left_navigation_visible(self) -> None:
        expect(self.nav_container).to_be_visible()
        expect(self.models_link).to_be_visible()
        expect(self.create_model_link).to_be_visible()
        expect(self.analytics_link).to_be_visible()
        expect(self.language_button).to_be_visible()
        expect(self.user_menu_button).to_be_visible()
        expect(self.collapse_button).to_be_visible()

    def go_to_dashboard(self) -> None:
        self.logo_link.click()

    def go_to_models(self) -> None:
        self.models_link.click()

    def go_to_create_model(self) -> None:
        self.create_model_link.click()

    def go_to_analytics(self) -> None:
        self.analytics_link.click()

    def go_to_batch_profile(self) -> None:
        self.batch_profile_link.click()