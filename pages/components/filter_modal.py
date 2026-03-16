from playwright.sync_api import Page, Locator, expect

class FilterModal:
    def __init__(self, page: Page) -> None:
        self.page = page

        # ===== Modal root =====
        # self.filter_modal: Locator = page.get_by_role("dialog")
        self.filter_modal: Locator = page.locator("div[role='dialog']")
        self.filter_title: Locator = page.get_by_role("heading", name="All filters")

        # ===== Footer buttons =====
        self.clear_all_button: Locator = self.filter_modal.get_by_role("button", name="Clear all")
        self.cancel_button: Locator = self.filter_modal.get_by_role("button", name="Cancel")
        self.apply_button: Locator = self.filter_modal.get_by_role("button", name="Apply")
        self.close_button: Locator = self.filter_modal.get_by_role("button", name="Close")

        # ===== Left filter categories =====
        self.owner_category: Locator = self.filter_modal.get_by_role("button", name="Owner")
        self.model_type_category: Locator = self.filter_modal.get_by_role("button", name="Model type")
        self.prediction_type_category: Locator = self.filter_modal.get_by_role("button", name="Prediction type")
        self.tag_category: Locator = self.filter_modal.get_by_role("button", name="Tag")

        self.lot_code_category: Locator = self.filter_modal.get_by_role("button", name="Lot code")
        self.main_operation_category: Locator = self.filter_modal.get_by_role("button", name="Main operation")
        self.measurement_operation_category: Locator = self.filter_modal.get_by_role("button", name="Measurement operation")
        self.measurement_parameters_category: Locator = self.filter_modal.get_by_role("button", name="Measurement parameters")
        self.relevant_operations_category: Locator = self.filter_modal.get_by_role("button", name="Relevant operations")

        self.model_status_category: Locator = self.filter_modal.get_by_role("button", name="Model status")
        self.publishing_status_category: Locator = self.filter_modal.get_by_role("button", name="Publishing status")
        self.score_category: Locator = self.filter_modal.get_by_role("button", name="Score")

        # ===== Common right panel =====
        self.search_input: Locator = self.filter_modal.locator("input[placeholder='Search']").first
        self.select_all_button: Locator = self.filter_modal.get_by_role("button", name="Select all")

        # ===== Owner options =====
        """
        hardcoding the checkbox locators for now since there are only 4 options. 
        If we find that these options are dynamic or there are more of them in the future, we can refactor to use a more flexible locator strategy.
        """
        self.owner_admin_checkbox: Locator = self.filter_modal.locator("#item-admin")
        self.owner_model_cauldron_checkbox: Locator = self.filter_modal.locator("#item-model_cauldron")
        self.owner_system_user_batch_model_create_checkbox: Locator = self.filter_modal.locator("#item-system_user_batch_model_create")
        self.owner_vmuser_checkbox: Locator = self.filter_modal.locator("#item-vmuser")

        self.owner_admin_label: Locator = self.filter_modal.locator("label[for='item-admin']")
        self.owner_model_cauldron_label: Locator = self.filter_modal.locator("label[for='item-model_cauldron']")
        self.owner_system_user_batch_model_create_label: Locator = self.filter_modal.locator("label[for='item-system_user_batch_model_create']")
        self.owner_vmuser_label: Locator = self.filter_modal.locator("label[for='item-vmuser']")

        # ===== Model type options =====
        self.model_type_automotive_checkbox: Locator = self.filter_modal.locator("#item-automotive")
        self.model_type_single_checkbox: Locator = self.filter_modal.locator("#item-single")
        self.model_type_single_sub_chamber_checkbox: Locator = self.filter_modal.locator("#item-single-sub-chamber")
        self.model_type_semi_batch_checkbox: Locator = self.filter_modal.locator("#item-semi-batch")
        self.model_type_multi_checkbox: Locator = self.filter_modal.locator("#item-multi")
        self.model_type_vector_thin_film_checkbox: Locator = self.filter_modal.locator("#item-vector-thin-film")
        self.model_type_vector_diffusion_checkbox: Locator = self.filter_modal.locator("#item-vector-diffusion")

        self.model_type_automotive_label: Locator = self.filter_modal.locator("label[for='item-automotive']")
        self.model_type_single_label: Locator = self.filter_modal.locator("label[for='item-single']")
        self.model_type_single_sub_chamber_label: Locator = self.filter_modal.locator("label[for='item-single-sub-chamber']")
        self.model_type_semi_batch_label: Locator = self.filter_modal.locator("label[for='item-semi-batch']")
        self.model_type_multi_label: Locator = self.filter_modal.locator("label[for='item-multi']")
        self.model_type_vector_thin_film_label: Locator = self.filter_modal.locator("label[for='item-vector-thin-film']")
        self.model_type_vector_diffusion_label: Locator = self.filter_modal.locator("label[for='item-vector-diffusion']")
        
        # ===== Prediction type options =====
        self.prediction_type_real_time_checkbox: Locator = self.filter_modal.locator("#item-real-time")
        self.prediction_type_deferred_h_checkbox: Locator = self.filter_modal.locator("#item-deferred-h")

        self.prediction_type_real_time_label: Locator = self.filter_modal.locator("label[for='item-real-time']")
        self.prediction_type_deferred_h_label: Locator = self.filter_modal.locator("label[for='item-deferred-h']")
    # =========================================================
    # Basic actions
    # =========================================================
    def verify_filter_modal_visible(self) -> None:
        expect(self.filter_modal).to_be_visible()
        expect(self.filter_title).to_be_visible()

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

    def verify_filter_modal_hidden(self) -> None:
        expect(self.filter_modal).not_to_be_visible()

    # =========================================================
    # Category navigation
    # =========================================================
    def select_owner(self) -> None:
        self.owner_category.click()
        expect(self.filter_modal.get_by_text("Owner", exact=True).last).to_be_visible()

    def select_model_type(self) -> None:
        self.model_type_category.click()
        expect(self.filter_modal.get_by_text("Model type", exact=True).last).to_be_visible()

    def select_prediction_type(self) -> None:
        self.prediction_type_category.click()
        expect(self.filter_modal.get_by_text("Prediction type", exact=True).last).to_be_visible()

    def select_tag_type(self) -> None:
        self.tag_category.click()
        expect(self.filter_modal.get_by_text("Tag", exact=True).last).to_be_visible()

    # =========================================================
    # Category option verification
    # =========================================================
    def verify_owner_options_visible(self) -> None:
        expect(self.owner_admin_checkbox).to_be_visible()
        expect(self.owner_model_cauldron_checkbox).to_be_visible()
        expect(self.owner_system_user_batch_model_create_checkbox).to_be_visible()
        expect(self.owner_vmuser_checkbox).to_be_visible()

        expect(self.owner_admin_label).to_be_visible()
        expect(self.owner_model_cauldron_label).to_be_visible()
        expect(self.owner_system_user_batch_model_create_label).to_be_visible()
        expect(self.owner_vmuser_label).to_be_visible()

    def verify_model_type_options_visible(self) -> None:
        expect(self.model_type_automotive_checkbox).to_be_visible()
        expect(self.model_type_single_checkbox).to_be_visible()
        expect(self.model_type_single_sub_chamber_checkbox).to_be_visible()
        expect(self.model_type_semi_batch_checkbox).to_be_visible()
        expect(self.model_type_multi_checkbox).to_be_visible()
        expect(self.model_type_vector_thin_film_checkbox).to_be_visible()
        expect(self.model_type_vector_diffusion_checkbox).to_be_visible()

        expect(self.model_type_automotive_label).to_be_visible()
        expect(self.model_type_single_label).to_be_visible()
        expect(self.model_type_single_sub_chamber_label).to_be_visible()
        expect(self.model_type_semi_batch_label).to_be_visible()
        expect(self.model_type_multi_label).to_be_visible()
        expect(self.model_type_vector_thin_film_label).to_be_visible()
        expect(self.model_type_vector_diffusion_label).to_be_visible()

    def verify_prediction_type_options_visible(self) -> None:
        expect(self.prediction_type_real_time_checkbox).to_be_visible()
        expect(self.prediction_type_deferred_h_checkbox).to_be_visible()

        expect(self.prediction_type_real_time_label).to_be_visible()
        expect(self.prediction_type_deferred_h_label).to_be_visible()

    # =========================================================
    # Search
    # =========================================================
    def search_filter_option(self, keyword: str) -> None:
        self.search_input.fill(keyword)

    def clear_search_filter_option(self) -> None:
        self.search_input.fill("")

    # =========================================================
    # Checkbox helpers
    # =========================================================
    def check_owner_admin(self) -> None:
        self.owner_admin_checkbox.click()

    def check_owner_option_one(self) -> None:
        self.owner_model_cauldron_checkbox.click()

    def check_owner_option_two(self) -> None:
        self.owner_system_user_batch_model_create_checkbox.click()

    def check_owner_option_three(self) -> None:
        self.owner_vmuser_checkbox.click()

    def check_model_type_automotive(self) -> None:
        self.model_type_automotive_checkbox.click()

    def check_model_type_single(self) -> None:
        self.model_type_single_checkbox.click()

    def check_model_type_single_sub_chamber(self) -> None:
        self.model_type_single_sub_chamber_checkbox.click()

    def check_model_type_semi_batch(self) -> None:
        self.model_type_semi_batch_checkbox.click()

    def check_model_type_multi(self) -> None:
        self.model_type_multi_checkbox.click()

    def check_model_type_vector_thin_film(self) -> None:
        self.model_type_vector_thin_film_checkbox.click()

    def check_model_type_vector_diffusion(self) -> None:
        self.model_type_vector_diffusion_checkbox.click()

    def check_prediction_type_real_time(self) -> None:
        self.prediction_type_real_time_checkbox.click()

    def check_prediction_type_deferred_h(self) -> None:
        self.prediction_type_deferred_h_checkbox.click()

    # =========================================================
    # Checked state helpers
    # =========================================================
    def verify_checkbox_checked(self, checkbox: Locator) -> None:
        expect(checkbox).to_have_attribute("aria-checked", "true")

    def verify_checkbox_unchecked(self, checkbox: Locator) -> None:
        expect(checkbox).to_have_attribute("aria-checked", "false")