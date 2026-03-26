from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage

class DashboardPage(BasePage):
    URL_PATH = "/"

    def __init__(self, page: Page, app_url: str, env_name: str) -> None:
        super().__init__(page, app_url, env_name)
        
        # === Main page / header ===
        self.main_content: Locator = page.locator("main")
        self.page_title: Locator = page.get_by_role("heading", name="dashboard")
        self.last_updated_text: Locator = page.locator("header span").filter(has_text="Last updated at:")

        # === Dashboard cards ===
        self.total_published_wafer_card: Locator = page.locator("div").filter(has=page.get_by_role("heading", name="Total Published Wafer Count (YTD)")).first
        self.recently_viewed_models_card: Locator = page.locator("div").filter(has=page.get_by_role("heading", name="recently viewed models")).first
        
        self.published_wafers_card = self._card_by_heading("published wafers")
        self.created_models_card = self._card_by_heading("created models")
        self.my_models_card = self._card_by_heading("my models")

        # === Total Published Wafer Count ===
        self.total_published_wafer_heading: Locator = page.get_by_role("heading", name="Total Published Wafer Count (YTD)")
        self.total_published_wafer_value: Locator = self.total_published_wafer_card.locator("p.text-\\[32px\\].font-bold")

        # === My Models ===
        self.my_models_heading: Locator = page.get_by_role("heading", name="my models")
        self.my_models_total_count: Locator = self.my_models_card.locator("p.text-primary-500")

        self.active_models_row: Locator = self.my_models_card.locator("li").filter(has=self.page.get_by_text("Active", exact=True))
        self.inactive_models_row: Locator = self.my_models_card.locator("li").filter(has=self.page.get_by_text("Inactive", exact=True))
        self.failed_models_row: Locator = self.my_models_card.locator("li").filter(has=self.page.get_by_text("Failed", exact=True))
        self.others_models_row: Locator = self.my_models_card.locator("li").filter(has=self.page.get_by_text("Others", exact=True))

        self.active_models_count: Locator = self.active_models_row.locator("button span").first
        self.inactive_models_count: Locator = self.inactive_models_row.locator("button span").first
        self.failed_models_count: Locator = self.failed_models_row.locator("button span").first
        self.others_models_count: Locator = self.others_models_row.locator("button span").first

        # Canvas chart inside My Models card
        self.my_models_donut_chart_canvas: Locator = self.my_models_card.locator("canvas").first

        # === Recently Viewed Models ===
        self.recently_viewed_models_heading: Locator = page.get_by_role("heading", name="recently viewed models")
        self.recently_viewed_models_list: Locator = self.recently_viewed_models_card.locator("ul")
        self.no_recently_viewed_models_text: Locator = self.recently_viewed_models_card.get_by_text("no recently viewed models", exact=False)

        # === Published Wafers ===
        self.published_wafers_heading: Locator = page.get_by_role("heading", name="published wafers")
        self.published_wafers_monthly_tab: Locator = self.published_wafers_card.get_by_role("button", name="monthly")
        self.published_wafers_weekly_tab: Locator = self.published_wafers_card.get_by_role("button", name="weekly")
        self.published_wafers_chart_container: Locator = self.published_wafers_card.locator("div[_echarts_instance_]")
        self.published_wafers_chart_chart_canvas: Locator = self.published_wafers_card.locator("canvas")

        # === Created Models ===
        self.created_models_heading: Locator = page.get_by_role("heading", name="created models")
        self.created_models_monthly_tab: Locator = self.created_models_card.get_by_role("button", name="monthly")
        self.created_models_weekly_tab: Locator = self.created_models_card.get_by_role("button", name="weekly")
        self.created_models_chart_container: Locator = self.created_models_card.locator("div[_echarts_instance_]")
        self.created_models_chart_canvas: Locator = self.created_models_card.locator("canvas")

    # ==========================================
    # Navigation / wait helpers
    # ==========================================
    def wait_for_page_to_load(self) -> None:
        expect(self.page_title).to_be_visible()
        expect(self.last_updated_text).to_be_visible()
        expect(self.total_published_wafer_heading).to_be_visible()
        expect(self.my_models_heading).to_be_visible()
        expect(self.recently_viewed_models_heading).to_be_visible()
        expect(self.published_wafers_heading).to_be_visible()
        expect(self.created_models_heading).to_be_visible()

    def verify_dashboard_page_loaded(self) -> None:
        self.wait_for_page_to_load()
        expect(self.page).not_to_have_url(f"{self.app_url}/login")

    # ==========================================
    # Assertions
    # ==========================================
    def verify_dashboard_core_widgets_visible(self) -> None:
        expect(self.last_updated_text).to_be_visible()
        expect(self.total_published_wafer_card).to_be_visible()
        expect(self.my_models_card).to_be_visible()
        expect(self.recently_viewed_models_card).to_be_visible()
        expect(self.published_wafers_card).to_be_visible()
        expect(self.created_models_card).to_be_visible()

    def verify_total_published_wafer_card_visible(self) -> None:
        expect(self.total_published_wafer_card).to_be_visible()
        expect(self.total_published_wafer_heading).to_be_visible()
        expect(self.total_published_wafer_value).to_be_visible()

    def verify_all_main_sections_visible(self) -> None:
        self.verify_my_models_sections_visible()
        self.verify_chart_selections_visible()

    def verify_my_models_sections_visible(self) -> None:
        expect(self.active_models_row).to_be_visible()
        expect(self.inactive_models_row).to_be_visible()
        expect(self.failed_models_row).to_be_visible()
        expect(self.others_models_row).to_be_visible()
        expect(self.my_models_donut_chart_canvas).to_be_visible()

    def verify_recently_viewed_models_section_visible(self) -> None:
        expect(self.recently_viewed_models_card).to_be_visible()
        expect(self.recently_viewed_models_heading).to_be_visible()

    def verify_recently_viewed_models_empty_state(self) -> None:
        expect(self.no_recently_viewed_models_text).to_be_visible()

    def verify_chart_selections_visible(self) -> None:
        expect(self.published_wafers_monthly_tab).to_be_visible()
        expect(self.published_wafers_weekly_tab).to_be_visible()
        expect(self.published_wafers_chart_container).to_be_visible()

        expect(self.created_models_monthly_tab).to_be_visible()
        expect(self.created_models_weekly_tab).to_be_visible()
        expect(self.created_models_chart_container).to_be_visible()

    def verify_total_published_wafer_count_visible(self) -> None:
        expect(self.total_published_wafer_heading).to_be_visible()
        expect(self.total_published_wafer_value).to_be_visible()

    # ==========================================
    # Read values
    # ==========================================
    def get_last_updated_text(self) -> str:
        return self.last_updated_text.inner_text().strip()
    
    def get_total_published_wafer_count(self) -> str:
        return self.total_published_wafer_value.inner_text().strip()
    
    def get_my_models_total_count(self) -> str:
        return self.my_models_total_count.inner_text().strip()

    def get_active_models_count(self) -> str:
        return self.active_models_count.inner_text().strip()
    
    def get_inactive_models_count(self) -> str:
        return self.inactive_models_count.inner_text().strip()
    
    def get_failed_models_count(self) -> str:
        return self.failed_models_count.inner_text().strip()
    
    def get_others_models_count(self) -> str:
        return self.others_models_count.inner_text().strip()
    
    # ==========================================
    # Actions
    # ==========================================
    def click_published_wafers_monthly(self) -> None:
        self.published_wafers_monthly_tab.click()
    
    def click_published_wafers_weekly(self) -> None:
        self.published_wafers_weekly_tab.click()
    
    def click_created_models_monthly(self) -> None:
        self.created_models_monthly_tab.click()
    
    def click_created_models_weekly(self) -> None:
        self.created_models_weekly_tab.click()
    
    def click_active_models(self) -> None:
        self.active_models_row.locator("button").click()
    
    def click_inactive_models(self) -> None:
        self.inactive_models_row.locator("button").click()
    
    def click_failed_models(self) -> None:
        self.failed_models_row.locator("button").click()
    
    def click_others_models(self) -> None:
        self.others_models_row.locator("button").click()

    def wait_for_dashboard_refresh(self) -> None:
        # Wait for the last updated text to change, indicating a refresh
        self.page.wait_for_load_state("networkidle")

    # ==========================================
    # Helper methods
    # ==========================================
    def _card_by_heading(self, heading_name: str) -> Locator:
        """
        Return the dashboard card container that belongs to the given heading
        This is needed because the structure of the dashboard cards is complex and we need to scope our locators within the specific card container to avoid ambiguity.
        """
        return self.page.get_by_role("heading", name=heading_name).locator("xpath=ancestor::div[contains(@class, 'bg-white')][1]")