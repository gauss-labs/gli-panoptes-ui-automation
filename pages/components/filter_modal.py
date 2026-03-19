import logging
import time
from typing import List, Optional

from playwright.sync_api import  Locator, Page, expect

logger = logging.getLogger(__name__)

class FilterModal:
    def __init__(self, page: Page) -> None:
        self.page = page

        # ===== Modal root =====
        self.filter_modal: Locator = page.locator("div[role='dialog']")
        self.filter_title: Locator = page.get_by_role("heading", name="All filters")

        # ===== Footer buttons =====
        self.clear_all_button: Locator = self.filter_modal.get_by_role("button", name="Clear all")
        self.cancel_button: Locator = self.filter_modal.get_by_role("button", name="Cancel")
        self.apply_button: Locator = self.filter_modal.get_by_role("button", name="Apply")
        self.close_button: Locator = self.filter_modal.get_by_role("button", name="Close")

        # ===== Common right panel =====
        self.search_input: Locator = self.filter_modal.locator("input[placeholder='Search']").first
        self.select_all_button: Locator = self.filter_modal.get_by_role("button", name="Select all")

        # ===== Filter options =====
        self.filter_option_labels: Locator = self.filter_modal.locator("label").filter(
            has=page.locator("input[type='checkbox']")
        )

    # =========================================================
    # Basic actions
    # =========================================================
    def verify_filter_modal_visible(self) -> None:
        expect(self.filter_modal).to_be_visible()
        expect(self.filter_title).to_be_visible()

    def verify_filter_modal_hidden(self) -> None:
        expect(self.filter_modal).not_to_be_visible()

    def click_select_all(self) -> None:
        self.select_all_button.click()

    def click_clear_all(self) -> None:
        self.clear_all_button.click()

    def click_apply(self) -> None:
        self.apply_button.click()

    def click_cancel(self) -> None:
        self.cancel_button.click()

    def close_filter_modal(self) -> None:
        self.close_button.click()

    # =========================================================
    # Category Helpers
    # =========================================================
    def right_panel(self) -> Locator:
        """
        Returns the right-side option panel of the filter modal.
        """
        return self.filter_modal.locator("section").nth(1)

    def category_button(self, category_name: str) -> Locator:
        """
        Returns the category button in the left filter panel by exact name.
        """
        left_panel = self.filter_modal.locator("section").first
        return left_panel.locator("button").filter(has_text=category_name).first

    def open_filter_category(self, category_name: str) -> None:
        """
        Opens the requested filter category from the left panel.
        """
        category = self.category_button(category_name)
        expect(category).to_be_visible()
        category.click()

        # Right panel heading should reflect the selected category.
        right_panel = self.filter_modal.locator("section").nth(1)
        expect(right_panel.get_by_text(category_name, exact=True)).to_be_visible()
        expect(self.search_input).to_be_visible()

        logger.info("Opened filter category: %s", category_name)

    def category_badge(self, category_name: str) -> Locator:
        """
        Returns the numeric badge shown inside the category button.
        Example: Owner -> 2
        """
        return self.category_button(category_name).locator("span.ml-auto")

    def get_category_selected_count(self, category_name: str) -> int:
        """
        Returns the selected count shown on the left category badge.
        """
        badge = self.category_badge(category_name)
        expect(badge).to_be_visible()

        badge_text = badge.inner_text().strip()
        logger.info("Category '%s' selected badge text: %s", category_name, badge_text)

        return int(badge_text)

    def verify_category_selected_count(self, category_name: str, expected_count: int) -> None:
        expect(self.category_badge(category_name)).to_have_text(str(expected_count))

    # =========================================================
    # Search Helpers
    # =========================================================
    def search_filter_option(self, keyword: str) -> None:
        self.search_input.fill(keyword)
        logger.info("Searched filter option with keyword: %s", keyword)
  
    def clear_search_filter_option(self) -> None:
        self.search_input.fill("")
        logger.info("Cleared filter option search input.")

    # =========================================================
    # Dynamic option helpers
    # =========================================================
    def option_checkboxes(self) -> Locator:
        """
        Returns all visible checkbox inputs in the currently opened filter category.
        """
        return self.right_panel().locator("button[role='checkbox'][id^='item-']")

    def option_labels(self) -> Locator:
        """
        Returns all visible labels associated with checkbox options
        in the currently opened filter category.
        """
        return self.filter_modal.locator("label[for^='item-']")

    def get_visible_filter_options(
        self,
        category_name: Optional[str] = None,
        min_expected: int = 1,
        timeout_ms: int = 10000,
    ) -> List[str]:
        if category_name:
            self.open_filter_category(category_name)

        end_time = time.time() + (timeout_ms / 1000)
        last_seen_options: List[str] = []

        while time.time() < end_time:
            option_labels = self.option_labels()
            count = option_labels.count()

            options = []
            for i in range(count):
                text = option_labels.nth(i).inner_text().strip()
                if text:
                    options.append(text)

            last_seen_options = options

            if len(options) >= min_expected:
                logger.info("Visible filter option count: %s", len(options))
                logger.info("Visible filter options: %s", options)
                return options

            self.page.wait_for_timeout(500)

        logger.info("Visible filter option count: %s", len(last_seen_options))
        logger.info("Visible filter options: %s", last_seen_options)

        raise AssertionError(
            "Expected at least %s visible filter options, but found %s."
            % (min_expected, len(last_seen_options))
        )
    def get_first_visible_filter_option(self, category_name: str, timeout_ms: int = 10000) -> str:
        return self.get_visible_filter_options(
            category_name=category_name,
            min_expected=1,
            timeout_ms=timeout_ms,
        )[0]

    def get_filter_option_count(self, category_name: Optional[str] = None) -> int:
        """
        Returns the number of visible options in the current or requested category.
        """
        options = self.get_visible_filter_options(category_name)
        return len(options)

    def option_checkbox_by_name(self, option_name: str) -> Locator:
        """
        Returns a checkbox locator for a given option name based on the checkbox id pattern.
        """
        return self.right_panel().locator(f"button[role='checkbox']#item-{option_name}").first

    def option_label_by_name(self, option_name: str) -> Locator:
        """
        Returns a label locator for a given option name.
        """
        return self.right_panel().locator(f"label[for='item-{option_name}']").first

    def verify_filter_options_visible(self, expected_options: List[str]) -> None:
        """
        Verifies that all expected options are visible in the current category.
        Use this only for categories whose values are stable across environments.
        """
        for option in expected_options:
            expect(self.option_checkbox_by_name(option)).to_be_visible()
            expect(self.option_label_by_name(option)).to_be_visible()

    def select_filter_option(self, option_name: str) -> None:
        """
        Selects a filter option by its exact option id/name.
        """
        checkbox = self.option_checkbox_by_name(option_name)
        expect(checkbox).to_be_visible()
        checkbox.click()
        expect(checkbox).to_have_attribute("aria-checked", "true")
        logger.info("Selected filter option: %s", option_name)

    def select_multiple_filter_options(self, category_name: str, option_names: List[str]) -> None:
        """
        Opens the given category and selects all provided option names.
        """
        self.open_filter_category(category_name)

        for option_name in option_names:
            self.select_filter_option(option_name)

        logger.info(
            "Selected multiple filter options from category '%s': %s",
            category_name,
            option_names,
        )

    def select_filter_option_if_exists(self, option_name: str, category_name: Optional[str] = None) -> bool:
        """
        Selects the option if it exists in the visible options list.
        Returns True if selected, otherwise False.
        """
        options = self.get_visible_filter_options(category_name)

        if option_name not in options:
            logger.warning("Option '%s' not found. Available options: %s", option_name, options)
            return False

        self.select_filter_option(option_name)
        return True

    def select_filter_option_with_fallback(
        self,
        category_name: str,
        preferred_option: Optional[str] = None,
    ) -> str:
        """
        Opens the category, selects the preferred option if available,
        otherwise selects the first available option.

        Returns the selected option text.
        """
        options = self.get_visible_filter_options(category_name)

        if not options:
            raise AssertionError(f"No options are displayed for filter category: {category_name}")

        if preferred_option and preferred_option in options:
            self.select_filter_option(preferred_option)
            logger.info("Selected preferred option '%s' from category '%s'.", preferred_option, category_name)
            return preferred_option

        fallback_option = options[0]
        self.select_filter_option(fallback_option)
        logger.info(
            "Preferred option '%s' not found in category '%s'. Selected fallback option '%s'.",
            preferred_option,
            category_name,
            fallback_option,
        )
        return fallback_option

    # =========================================================
    # Checked state helpers
    # =========================================================
    def verify_checkbox_checked(self, checkbox: Locator) -> None:
        expect(checkbox).to_have_attribute("aria-checked", "true")

    def verify_checkbox_unchecked(self, checkbox: Locator) -> None:
        expect(checkbox).to_have_attribute("aria-checked", "false")

    # =========================================================
    # Selected summary helpers
    # =========================================================
    def selected_summary_container(self) -> Locator:
        """
        Container row that shows '<count> Selected' and 'Select all'.
        """
        return self.filter_modal.locator("div.border-y.border-neutral-300").first

    def selected_summary_count_text(self) -> Locator:
        """
        Bold numeric text only. Example: '2'
        """
        return self.selected_summary_container().locator("span.font-bold.text-neutral-700")

    def selected_summary_text(self) -> Locator:
        """
        Whole summary text. Example: '2 Selected'
        """
        return self.selected_summary_container().locator("div.flex.items-center.gap-0\\.5")

    def get_selected_summary_count(self) -> int:
        count_text = self.selected_summary_count_text().inner_text().strip()
        logger.info("Selected summary count text: %s", count_text)
        return int(count_text)

    def verify_selected_summary_count(self, expected_count: int) -> None:
        expect(self.selected_summary_count_text()).to_have_text(str(expected_count))
        expect(self.selected_summary_text()).to_contain_text("Selected")

    # =========================================================
    # Selected chip helpers
    # =========================================================
    def selected_filter_chips(self) -> Locator:
        """
        Selected filter chips shown in the footer area.
        """
        return self.filter_modal.locator("div.flex.max-h-20.flex-wrap.gap-2.overflow-y-auto > span")

    def get_selected_filter_chip_texts(self) -> List[str]:
        chips = self.selected_filter_chips()
        count = chips.count()

        values: List[str] = []
        for i in range(count):
            text = chips.nth(i).inner_text().strip()
            if text:
                values.append(text)

        logger.info("Selected chip count: %s", len(values))
        logger.info("Selected chip texts: %s", values)
        return values