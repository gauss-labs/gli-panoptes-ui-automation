import re

import pytest
from playwright.sync_api import expect, Page

from pages.login_page import LoginPage
from pages.models_page import ModelsPage

@pytest.fixture
def models_page(logged_in_page, app_url: str, env_name: str) -> ModelsPage:
    """
    Logs in first, then returns the Models page object.
    """
    models_page = ModelsPage(logged_in_page, app_url, env_name)
    models_page.left_navigation.go_to_models()
    models_page.wait_for_page_to_load()

    return models_page

def assert_result_summary_format(summary: str) -> None:
    assert "of" in summary
    assert "models" in summary
    assert re.search(r"\d+\s*-\s*\d+\s*of\s*\d+\s*models", summary), (
        f"Unexpected result summary format: '{summary}'"
    )

@pytest.mark.smoke
@pytest.mark.models
def test_verify_models_page_loads_successfully(models_page: ModelsPage) -> None:
    """
    Verify that the Models page loads successfully after login.
    """
    models_page.verify_models_page_loaded()
    models_page.verify_search_input_visible()
    models_page.verify_filter_button_visible()
    models_page.verify_table_visible()
    models_page.verify_result_summary_visible()

@pytest.mark.smoke
@pytest.mark.models
def test_verify_models_page_header_elements_visible(models_page: ModelsPage) -> None:
    """
    Verify that the main header elements of the Models page are visible.
    """
    models_page.verify_header_elements_visible()

@pytest.mark.smoke
@pytest.mark.models
def test_verify_toolbar_controls_visible(models_page: ModelsPage) -> None:
    """
    Verify that the toolbar controls (Performance Window dropdown, Accuracy/Performance toggle button, Quickview switch) are visible on the Models page.
    """
    models_page.verify_toolbar_controls_visible()

@pytest.mark.smoke
@pytest.mark.models
def test_verify_result_summary_displays_model_count(models_page: ModelsPage) -> None:
    """
    Verify that the result summary text displays the model count in the expected format (e.g., "1-20 of 100 models").
    """
    summary = models_page.get_result_summary_text()
    assert_result_summary_format(summary)
    
@pytest.mark.regression
@pytest.mark.models
def test_search_existing_model(models_page: ModelsPage, model_test_data: dict, env_name: str) -> None:
    """
    Verify that searching for an existing model name returns the correct result in the table.
    """
    model_name = model_test_data["models_search"][env_name]["existing_model_name"]

    models_page.search_model(model_name)
    models_page.verify_search_value(model_name)
    models_page.verify_model_present_in_table(model_name)

@pytest.mark.regression
@pytest.mark.models
def test_search_partial_model_name(models_page: ModelsPage, model_test_data: dict, env_name: str) -> None:
    partial_name = model_test_data["models_search"][env_name]["partial_model_name"]
    """
    Verify that searching with a partial model name returns relevant results in the table.
    """
    models_page.search_model(partial_name)
    models_page.verify_search_value(partial_name)
    models_page.wait_for_partial_search_results(partial_name)
    
    row_count = models_page.table_rows.filter(has_text=partial_name).count()
    assert row_count > 0

@pytest.mark.regression
@pytest.mark.models
def test_search_non_existing_model(models_page: ModelsPage, model_test_data: dict, env_name: str) -> None:
    """
    Verify that searching for a non-existing model name results in no matches found in the table.
    """
    non_existing_name = model_test_data["models_search"][env_name]["non_existing_model_name"]

    models_page.search_model(non_existing_name)
    models_page.verify_search_value(non_existing_name)

    row_count = models_page.table_rows.count()
    assert row_count == 0

@pytest.mark.regression
@pytest.mark.models
def test_clear_search_input(models_page: ModelsPage, model_test_data: dict, env_name: str) -> None:
    """
    Verify that clearing the search input resets the table results and the search input value.
    """
    model_name = model_test_data["models_search"][env_name]["existing_model_name"]

    models_page.search_model(model_name)
    models_page.verify_search_value(model_name)

    models_page.clear_search()
    models_page.verify_search_value("")

@pytest.mark.regression
@pytest.mark.models
def test_verify_known_model_details_and_expand(models_page: ModelsPage, model_test_data: dict, env_name: str) -> None:    
    """
    Verify that a known model row is visible, contains correct metadata,
    and can be expanded to reveal child model units.
    """
    details_data = model_test_data["known_model_details"][env_name]

    model_name = details_data["model_name"]
    child_row_texts = details_data["child_row_texts"]
    expected_status = details_data["expected_status"]
    expected_owner = details_data["expected_owner"]

    # Verify row is visible
    models_page.verify_row_visible(model_name)

    # Verify model status
    status = models_page.get_model_status(model_name)
    assert status.lower() == expected_status.lower()

    # Verify owner
    owner = models_page.get_owner(model_name)
    assert owner.lower() == expected_owner.lower()

    # Expand parent model row
    models_page.expand_model_row(model_name)

    # Verify child row appears
    for child_row_text in child_row_texts:
        models_page.verify_row_visible(child_row_text)

@pytest.mark.regression
@pytest.mark.models
def test_select_single_row(models_page: ModelsPage, model_test_data: dict, env_name: str) -> None:
    """
    Verify that selecting a single model row by clicking its checkbox works correctly.
    """
    row_text = model_test_data["known_model_details"][env_name]["model_name"]

    models_page.select_row(row_text)
    checkbox = models_page.get_row_checkbox(row_text)

    assert checkbox.get_attribute("aria-checked") == "true"

@pytest.mark.regression
@pytest.mark.models
def test_verify_previous_pagination_buttons_disabled_on_first_page(models_page: ModelsPage) -> None:
    """
    Verify that the "Previous" pagination button is disabled on the first page of results.
    """
    assert models_page.is_previous_page_enabled() is False

@pytest.mark.regression
@pytest.mark.models
def test_go_to_next_page(models_page: ModelsPage) -> None:
    """
    Verify that clicking the "Next" pagination button navigates to the next page of results and updates the result summary text.
    """
    initial_summary = models_page.get_result_summary_text()

    if models_page.is_next_page_enabled():
        models_page.go_to_next_page()
        new_summary = models_page.get_result_summary_text()
        assert new_summary != initial_summary
    else:
        pytest.skip("Only one page of results.")

@pytest.mark.regression
@pytest.mark.models
def test_toggle_quickview(models_page: ModelsPage) -> None:
    """
    Verify that toggling the Quickview switch changes its state accordingly.
    """
    initial_state = models_page.is_quickview_enabled()

    if initial_state:
        models_page.disable_quickview()
        assert models_page.is_quickview_enabled() is False
    else:
        models_page.enable_quickview()
        assert models_page.is_quickview_enabled() is True
