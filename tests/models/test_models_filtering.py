import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.models_page import ModelsPage
from pages.components.filter_modal import FilterModal

@pytest.fixture
def models_page(page: Page, app_url: str) -> ModelsPage:
    """
    Logs in first, then navigates to the Models page.
    """
    login_page = LoginPage(page, app_url)
    login_page.navigate()
    login_page.login("admin", "gausslabs")

    models_page = ModelsPage(page, app_url)
    models_page.left_navigation.go_to_models()
    models_page.wait_for_page_to_load()

    return models_page

@pytest.fixture
def filter_modal(models_page: ModelsPage) -> FilterModal:
    """
    Opens the filter modal from the Models page and returns the modal page object.
    """
    models_page.filter_button.click()

    filter_modal = FilterModal(models_page.page)
    filter_modal.verify_filter_modal_visible()

    return filter_modal

# @pytest.fixture
# def filter_modal(page: Page) -> FilterModal:
#     return FilterModal(page)

# =========================================================
# Basic modal tests
# =========================================================
@pytest.mark.regression
@pytest.mark.models
def test_verify_filter_modal_opens(models_page: ModelsPage, filter_modal: FilterModal):
    """
    Verify that the filter modal opens when the filter button is clicked and that the main elements of the modal are visible.
    """
    filter_modal.verify_filter_modal_visible()

@pytest.mark.regression
@pytest.mark.models
def test_verify_filter_modal_closes_with_close_button(filter_modal: FilterModal):
    """
    Verify that the filter modal closes when the close button is clicked.
    """
    filter_modal.close_filter_modal()
    filter_modal.verify_filter_modal_hidden()

@pytest.mark.regression
@pytest.mark.models
def test_verify_filter_modal_closes_with_cancel_button(filter_modal: FilterModal):
    """
    Verify that the filter modal closes when the cancel button is clicked.
    """
    filter_modal.click_cancel()
    filter_modal.verify_filter_modal_hidden()

# =========================================================
# Owner category tests
# =========================================================
@pytest.mark.regression
@pytest.mark.models
def test_verify_owner_filter_options_visible(filter_modal: FilterModal):
    """
    Verify that the Owner filter options are visible when the Owner category is selected.
    """
    filter_modal.select_owner()
    filter_modal.verify_owner_options_visible()

@pytest.mark.regression
@pytest.mark.models
def test_verify_owner_filter_search_works(filter_modal: FilterModal):
    """
    Verify that the search functionality in the Owner filter category works as expected.
    """
    filter_modal.select_owner()
    filter_modal.search_filter_option("admin")

    expect(filter_modal.owner_admin_label).to_be_visible()
    expect(filter_modal.owner_model_cauldron_label).not_to_be_visible()

@pytest.mark.regression
@pytest.mark.models
def test_verify_owner_checkbox_can_be_selected(filter_modal: FilterModal):
    """
    Verify that the checkbox for an Owner filter option can be selected and that it reflects the checked state.
    """
    filter_modal.select_owner()
    filter_modal.check_owner_admin()
    filter_modal.verify_checkbox_checked(filter_modal.owner_admin_checkbox)

@pytest.mark.regression
@pytest.mark.models
def test_verify_owner_select_all_checks_all_options(filter_modal: FilterModal):
    filter_modal.select_owner()
    filter_modal.click_select_all()

    filter_modal.verify_checkbox_checked(filter_modal.owner_admin_checkbox)
    filter_modal.verify_checkbox_checked(filter_modal.owner_model_cauldron_checkbox)
    filter_modal.verify_checkbox_checked(filter_modal.owner_system_user_batch_model_create_checkbox)
    filter_modal.verify_checkbox_checked(filter_modal.owner_vmuser_checkbox)