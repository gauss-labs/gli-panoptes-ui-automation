import pytest
import logging
from playwright.sync_api import Page, expect
from pytest_playwright.pytest_playwright import page

from pages.login_page import LoginPage
from pages.models_page import ModelsPage
from pages.components.filter_modal import FilterModal

logger = logging.getLogger(__name__)

@pytest.fixture
def models_page(logged_in_page, app_url: str) -> ModelsPage:
    """
    Logs in first, then navigates to the Models page.
    """
    models_page = ModelsPage(logged_in_page, app_url)
    models_page.left_navigation.go_to_models()
    models_page.wait_for_page_to_load()

    return models_page

@pytest.fixture
def filter_modal(models_page: ModelsPage) -> FilterModal:
    """
    Opens the filter modal from the Models page and returns the modal page object.
    """
    models_page.filter_button.click()

    modal = FilterModal(models_page.page)
    modal.verify_filter_modal_visible()

    return modal

# =========================================================
# Basic modal tests
# =========================================================
@pytest.mark.regression
@pytest.mark.models
def test_verify_filter_modal_opens(filter_modal: FilterModal):
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
def test_verify_owner_filter_options_are_loaded(filter_modal: FilterModal) -> None:
    """
    Verify that the Owner category loads at least one visible option.
    This test is environment-safe since option values may differ by environment.
    """
    owner_options = filter_modal.get_visible_filter_options("Owner")

    logger.info("Owner options count: %s", len(owner_options))
    logger.info("Owner options: %s", owner_options)
    print(f"Owner options count: {len(owner_options)}")
    print(f"Owner options: {owner_options}")

    assert len(owner_options) > 0, "Expected at least one Owner filter option to be displayed."

@pytest.mark.regression
@pytest.mark.models
def test_verify_owner_filter_search_works_for_existing_option(filter_modal: FilterModal) -> None:
    """
    Verify that Owner search narrows results correctly using a runtime-discovered option.
    """
    owner_options = filter_modal.get_visible_filter_options("Owner")
    target_option = owner_options[0]

    filter_modal.search_filter_option(target_option)

    expect(filter_modal.option_label_by_name(target_option)).to_be_visible()
    filtered_options = filter_modal.get_visible_filter_options()
    assert target_option in filtered_options

@pytest.mark.regression
@pytest.mark.models
def test_verify_owner_checkbox_can_be_selected(filter_modal: FilterModal) -> None:
    """
    Verify that an Owner checkbox can be selected using a runtime-discovered option.
    """
    target_option = filter_modal.get_first_visible_filter_option("Owner")
    filter_modal.select_filter_option(target_option)
    filter_modal.verify_checkbox_checked(filter_modal.option_checkbox_by_name(target_option))

@pytest.mark.regression
@pytest.mark.models
def test_verify_owner_filter_search_works(filter_modal: FilterModal):
    """
    Verify that the search functionality in the Owner filter category works as expected.
    """
    owner_options = filter_modal.get_visible_filter_options("Owner")
    assert len(owner_options) > 0, "Expected at least one Owner option to be displayed."

    target_option = owner_options[0]
    filter_modal.search_filter_option(target_option)

    filtered_options = filter_modal.get_visible_filter_options()

    assert target_option in filtered_options
    assert len(filtered_options) == 1

@pytest.mark.regression
@pytest.mark.models
def test_log_owner_filter_options(filter_modal: FilterModal):
    owner_options = filter_modal.get_visible_filter_options("Owner")

    assert len(owner_options) > 0
    print(f"Owner options count: {len(owner_options)}")
    print(f"Owner options: {owner_options}")

@pytest.mark.regression
@pytest.mark.models
def test_verify_owner_category_selection_count_updates_for_single_selection(
    filter_modal: FilterModal,
) -> None:
    """
    Verify that the Owner category badge count, selected summary count,
    and selected chip area update correctly after selecting one Owner option.
    """
    owner_options = filter_modal.get_visible_filter_options("Owner")
    assert len(owner_options) > 0, "Expected at least one Owner option to be displayed."

    selected_option = owner_options[0]
    filter_modal.select_filter_option(selected_option)

    filter_modal.verify_checkbox_checked(filter_modal.option_checkbox_by_name(selected_option))
    filter_modal.verify_selected_summary_count(1)
    filter_modal.verify_category_selected_count("Owner", 1)

    chip_texts = filter_modal.get_selected_filter_chip_texts()
    assert len(chip_texts) == 1
    assert any(selected_option in chip for chip in chip_texts), (
        f"Expected selected chip to contain option: {selected_option}"
    )

@pytest.mark.regression
@pytest.mark.models
def test_verify_owner_category_selection_count_updates_for_multiple_selections(
    filter_modal: FilterModal,
) -> None:
    """
    Verify that the Owner category badge count, selected summary count,
    and selected chips update correctly after selecting multiple Owner options.
    """
    owner_options = filter_modal.get_visible_filter_options("Owner")

    if len(owner_options) < 2:
        pytest.skip("This environment has fewer than 2 Owner options.")

    selected_options = owner_options[:2]
    filter_modal.select_multiple_filter_options("Owner", selected_options)

    filter_modal.verify_selected_summary_count(2)
    filter_modal.verify_category_selected_count("Owner", 2)

    chip_texts = filter_modal.get_selected_filter_chip_texts()
    assert len(chip_texts) == 2

    for option in selected_options:
        assert any(option in chip for chip in chip_texts), (
            f"Expected selected chip to contain option: {option}"
        )

@pytest.mark.regression
@pytest.mark.models
def test_verify_owner_select_all_checks_all_visible_options(filter_modal: FilterModal) -> None:
    """
    Verify that Select all checks all visible Owner options and that the selected counts 
    are updated correctly across the modal UI.
    """
    owner_options = filter_modal.get_visible_filter_options("Owner")
    expected_count = len(owner_options)

    assert expected_count > 0, "Expected at least one visible Owner option."

    filter_modal.click_select_all()

    for option in owner_options:
        filter_modal.verify_checkbox_checked(filter_modal.option_checkbox_by_name(option))

    filter_modal.verify_selected_summary_count(expected_count)
    filter_modal.verify_category_selected_count("Owner", expected_count)

    chip_texts = filter_modal.get_selected_filter_chip_texts()
    assert len(chip_texts) == expected_count

    for option in owner_options:
        assert any(option in chip for chip in chip_texts), (
            f"Expected selected chip to contain option: {option}"
        )