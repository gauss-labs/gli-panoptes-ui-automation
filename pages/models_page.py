from __future__ import annotations

from email.mime import text
import re
from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage

class ModelsPage(BasePage):
    URL_PATH = "/models"

    def __init__(self, page: Page, app_url: str):
        super().__init__(page, app_url)

        # ===== Page / header =====
        self.main_content: Locator = page.locator("main")
        self.page_title: Locator = page.locator("main h1").filter(has_text="models")
        self.create_model_button: Locator = page.get_by_role("button", name=re.compile(r"create model", re.I))

        # ===== Top controls =====
        # Opens the "All filters" dialog/modal.
        self.filter_button: Locator = page.locator("button[aria-haspopup='dialog']").first

        # Saved filter-set dropdown (currently "Select filter set").
        self.filter_set_dropdown: Locator = page.get_by_role("button", name=re.compile(r"select filter set", re.I))

         # Search input for model name search.
        self.search_input: Locator = page.get_by_placeholder("Search the model name")

        # Small clear button inside search input (hidden until text exists).
        self.search_clear_button: Locator = self.search_input.locator("xpath=following-sibling::div//button")

        # ===== Toolbar controls =====
        self.sort_up_down_button: Locator = page.locator("section").filter(
            has=page.get_by_role("combobox", name=re.compile(r"performance window", re.I))
        ).locator("button").nth(0)

        self.collapse_expand_button: Locator = page.locator("section").filter(
            has=page.get_by_role("combobox", name=re.compile(r"performance window", re.I))
        ).locator("button").nth(1)

        self.performance_window_dropdown: Locator = page.locator("button[role='combobox']").filter(has_text="Performance window")
        # self.performance_window_dropdown: Locator = page.get_by_role("combobox", name=re.compile(r"performance window", re.I))
        self.accuracy_performance_button: Locator = page.get_by_role("button", name=re.compile(r"accuracy performance", re.I))
        self.quickview_switch: Locator = page.get_by_role("switch")

        # ===== Pagination / summary =====
        self.result_summary_text: Locator = page.locator("p.text-caption").filter(has_text="of")
        self.pagination_container: Locator = self.result_summary_text.locator("xpath=..")

        self.first_page_button: Locator = self.pagination_container.locator("button").nth(0)
        self.previous_page_button: Locator = self.pagination_container.locator("button").nth(1)
        self.next_page_button: Locator = self.pagination_container.locator("button").nth(2)
        self.last_page_button: Locator = self.pagination_container.locator("button").nth(3)
 
        # ===== Table =====
        self.models_table: Locator = page.locator("table").first
        self.table_header: Locator = self.models_table.locator("thead")
        self.table_body: Locator = self.models_table.locator("tbody")
        self.table_rows: Locator = self.table_body.locator("tr")

        self.select_all_checkbox: Locator = page.get_by_role("checkbox", name="Select all")

        # ===== Common column headers =====
        self.model_name_header: Locator = page.get_by_role("columnheader", name=re.compile(r"model name", re.I))
        self.model_status_header: Locator = page.get_by_role("columnheader", name=re.compile(r"model status", re.I))
        self.owner_header: Locator = page.get_by_role("columnheader", name=re.compile(r"owner", re.I))
        self.tag_header: Locator = page.get_by_role("columnheader", name=re.compile(r"tag", re.I))
        self.model_type_header: Locator = page.get_by_role("columnheader", name=re.compile(r"model type", re.I))
        self.pred_type_header: Locator = page.get_by_role("columnheader", name=re.compile(r"pred\\. type", re.I))
        self.created_at_header: Locator = page.get_by_role("button", name=re.compile(r"created at", re.I))

    # ---------------------------------------------------------------------
    # Navigation / page state
    # ---------------------------------------------------------------------
    def navigate(self) -> None:
        super().navigate(self.URL_PATH)
        self.wait_for_page_to_load()

    def wait_for_page_to_load(self) -> None:
        expect(self.page_title).to_be_visible()
        expect(self.search_input).to_be_visible()
        expect(self.models_table).to_be_visible()

    def verify_models_page_loaded(self) -> None:
        self.wait_for_page_to_load()
        expect(self.page).to_have_url(re.compile(rf"{re.escape(self.app_url.rstrip('/'))}/models/?$"))

    # ---------------------------------------------------------------------
    # Search
    # ---------------------------------------------------------------------
    def search_model(self, model_name: str) -> None:
        expect(self.search_input).to_be_visible()
        self.search_input.fill(model_name)

    def clear_search(self) -> None:
        self.search_input.fill("")
        expect(self.search_input).to_have_value("")

    def get_search_value(self) -> str:
        return self.search_input.input_value()
    
    def wait_for_partial_search_results(self, text: str) -> None:   
        expect(self.table_rows.filter(has_text=text).first).to_be_visible()

    # ---------------------------------------------------------------------
    # Filters / controls
    # ---------------------------------------------------------------------
    def open_filter_modal(self) -> None:
        self.filter_button.click()

    def open_filter_set_dropdown(self) -> None:
        self.filter_set_dropdown.click()

    def open_performance_window_dropdown(self) -> None:
        self.performance_window_dropdown.click()

    def click_accuracy_performance(self) -> None:
        self.accuracy_performance_button.click()

    def enable_quickview(self) -> None:
        if self.quickview_switch.get_attribute("aria-checked") != "true":
            self.quickview_switch.click()

    def disable_quickview(self) -> None:
        if self.quickview_switch.get_attribute("aria-checked") != "false":
            self.quickview_switch.click()

    def is_quickview_enabled(self) -> bool:
        return self.quickview_switch.get_attribute("aria-checked") == "true"
    
    # ---------------------------------------------------------------------
    # Pagination
    # ---------------------------------------------------------------------
    def get_result_summary_text(self) -> str:
        return self.result_summary_text.first.inner_text().strip()

    def go_to_next_page(self) -> None:
        self.next_page_button.click()

    def go_to_previous_page(self) -> None:
        self.previous_page_button.click()

    def go_to_first_page(self) -> None:
        self.first_page_button.click()

    def go_to_last_page(self) -> None:
        self.last_page_button.click()

    def is_next_page_enabled(self) -> bool:
        return self.next_page_button.is_enabled()

    def is_previous_page_enabled(self) -> bool:
        return self.previous_page_button.is_enabled()

    # ---------------------------------------------------------------------
    # Table helpers
    # ---------------------------------------------------------------------
    def get_row_by_text(self, text: str) -> Locator:
        return self.table_rows.filter(has_text=text).first

    def get_model_link(self, model_name: str) -> Locator:
        return self.page.get_by_role("link", name=re.compile(re.escape(model_name), re.I)).first

    def get_model_parent_row(self, model_name: str) -> Locator:
        # Parent model rows have an expand/collapse chevron button before the model link.
        row = self.table_rows.filter(
            has=self.page.get_by_role("link", name=re.compile(re.escape(model_name), re.I))
        ).first
        return row

    def get_model_unit_row(self, model_unit_name: str) -> Locator:
        return self.table_rows.filter(
            has=self.page.get_by_role("link", name=re.compile(re.escape(model_unit_name), re.I))
        ).first

    def click_model_link(self, model_name: str) -> None:
        self.get_model_link(model_name).click()

    def expand_model_row(self, model_name: str) -> None:
        row = self.get_model_parent_row(model_name)
        expand_button = row.locator("button").first
        expand_button.click()

    def get_row_checkbox(self, row_text: str) -> Locator:
        row = self.get_row_by_text(row_text)
        return row.get_by_role("checkbox", name="Select row")

    def select_row(self, row_text: str) -> None:
        checkbox = self.get_row_checkbox(row_text)
        if checkbox.get_attribute("aria-checked") != "true":
            checkbox.click()

    def unselect_row(self, row_text: str) -> None:
        checkbox = self.get_row_checkbox(row_text)
        if checkbox.get_attribute("aria-checked") == "true":
            checkbox.click()

    def get_row_action_menu_button(self, row_text: str) -> Locator:
        row = self.get_row_by_text(row_text)
        return row.locator("button[aria-haspopup='menu']").last

    def open_row_action_menu(self, row_text: str) -> None:
        self.get_row_action_menu_button(row_text).click()

    # ---------------------------------------------------------------------
    # Row data helpers
    # ---------------------------------------------------------------------
    def get_row_cells(self, row_text: str) -> list[str]:
        row = self.get_row_by_text(row_text)
        return [cell.inner_text().strip() for cell in row.locator("td").all()]

    def get_model_status(self, row_text: str) -> str:
        row = self.get_row_by_text(row_text)
        # Status pill is usually in the 3rd td.
        return row.locator("td").nth(2).inner_text().strip()

    def get_owner(self, row_text: str) -> str:
        row = self.get_row_by_text(row_text)
        # Owner is typically after status.
        return row.locator("td").nth(3).inner_text().strip()

    def get_created_at(self, row_text: str) -> str:
        row = self.get_row_by_text(row_text)
        # Created-at is near the last columns.
        return row.locator("td").nth(-2).inner_text().strip()

    def is_row_visible(self, row_text: str) -> bool:
        return self.get_row_by_text(row_text).is_visible()

    def verify_row_visible(self, row_text: str) -> None:
        expect(self.get_row_by_text(row_text)).to_be_visible()

    def verify_row_not_visible(self, row_text: str) -> None:
        expect(self.get_row_by_text(row_text)).not_to_be_visible()

    # ---------------------------------------------------------------------
    # Bulk selection
    # ---------------------------------------------------------------------
    def select_all_rows(self) -> None:
        if self.select_all_checkbox.get_attribute("aria-checked") != "true":
            self.select_all_checkbox.click()

    def unselect_all_rows(self) -> None:
        if self.select_all_checkbox.get_attribute("aria-checked") == "true":
            self.select_all_checkbox.click()

    # ---------------------------------------------------------------------
    # Assertions
    # ---------------------------------------------------------------------
    def verify_search_input_visible(self) -> None:
        expect(self.search_input).to_be_visible()

    def verify_filter_button_visible(self) -> None:
        expect(self.filter_button).to_be_visible()

    def verify_table_visible(self) -> None:
        expect(self.models_table).to_be_visible()

    def verify_result_summary_visible(self) -> None:
        expect(self.result_summary_text.first).to_be_visible()

    def verify_model_present_in_table(self, model_name: str) -> None:
        expect(self.get_model_link(model_name)).to_be_visible()

    def verify_search_value(self, expected_value: str) -> None:
        expect(self.search_input).to_have_value(expected_value)