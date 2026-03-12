from playwright.sync_api import Page, Locator, expect

class FilterModel:
    def __init__(self, page: Page) -> None:
        self.page = page

        # modal
        self.filter_modal: Locator = page.get_by_role("dialog")
        self.filter_title: Locator = page.get_by_role("heading", name="All filters")

        # left filter categories
        self.owner_filter_button: Locator = page.get_by_role("button", name="Owner")
        self.model_type_filter_button: Locator = page.get_by_role("button", name="Model type")
        self.prediction_type_filter_button: Locator = page.get_by_role("button", name="Prediction type")
        self.tag_filter_button: Locator = page.get_by_role("button", name="Tag")
        self.model_status_filter_button: Locator = page.get_by_role("button", name="Model status")
        self.publishing_status_filter_button: Locator = page.get_by_role("button", name="Publishing status")
        self.score_filter_button: Locator = page.get_by_role("button", name="Score")

        # search inside selected filter panel
        self.filter_search_input: Locator = self.filter_modal.get_by_placeholder("Search")

        # footer buttons
        self.select_all_button: Locator = self.filter_modal.get_by_role("button", name="Select all")
        self.clear_all_button: Locator = self.filter_modal.get_by_role("button", name="Clear all")
        self.cancel_button: Locator = self.filter_modal.get_by_role("button", name="Cancel")
        self.apply_button: Locator = self.filter_modal.get_by_role("button", name="Apply")
        self.close_button: Locator = self.filter_modal.get_by_role("button", name="Close")

    def verify_filter_modal_visible(self) -> None:
        expect(self.filter_modal).to_be_visible()
        expect(self.filter_title).to_be_visible()

    def open_owner_filter(self) -> None:
        self.owner_filter_button.click()

    def search_filter_option(self, value: str) -> None:
        self.filter_search_input.fill(value)

    def select_filter_option_by_label(self, value: str) -> None:
        self.filter_modal.locator(f"label[for='item-{value}']").click()

    def select_filter_option_by_checkbox_id(self, value: str) -> None:
        self.filter_modal.locator(f"#item-{value}").click()

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