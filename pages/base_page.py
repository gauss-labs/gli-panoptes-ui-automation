from __future__ import annotations

from playwright.sync_api import Page
from pages.components.left_navigation import LeftNavigation

class BasePage:
    def __init__(self, page: Page, app_url: str):
        self.page = page
        self.app_url = app_url
        self.left_navigation = LeftNavigation(page)

    def navigate(self, path: str) -> None:
        self.page.goto(f"{self.app_url}{path}")