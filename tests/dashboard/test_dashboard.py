import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.fixture
def logged_in_dashboard(logged_in_page, app_url: str) -> DashboardPage:
    dashboard_page = DashboardPage(logged_in_page, app_url)
    dashboard_page.verify_dashboard_page_loaded()

    return dashboard_page
# @pytest.fixture
# def logged_in_dashboard(page: Page, app_url: str) -> DashboardPage:
#     """
#     Logs into the application and lands on Dashboard page.
#     Returns DashboardPage object for reuse in tests.
#     """
#     login_page = LoginPage(page, app_url)
#     dashboard_page = DashboardPage(page, app_url)

#     login_page.navigate()
#     login_page.login("admin", "gausslabs")

#     dashboard_page.verify_dashboard_page_loaded()
#     return dashboard_page

# =========================================================
# Smoke / Page Load
# =========================================================
@pytest.mark.smoke
@pytest.mark.dashboard
def test_dashboard_page_loads_successfully(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that Dashboard page loads successfully after login.
    """
    logged_in_dashboard.verify_dashboard_page_loaded()

@pytest.mark.smoke
@pytest.mark.dashboard
def test_dashboard_header_is_visible(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that the main header of the dashboard is visible.
    """
    logged_in_dashboard.verify_dashboard_header_visible()
# =========================================================
# Core Widget Visibility
# =========================================================
@pytest.mark.regression
@pytest.mark.dashboard
def test_dashboard_core_widgets_are_visible(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that the core widgets of the dashboard (Total Published Wafer Count, Published Wafers chart, Created Models chart) are visible.
    """
    logged_in_dashboard.verify_dashboard_core_widgets_visible()

@pytest.mark.regression
@pytest.mark.dashboard
def test_all_main_dashboard_sections_are_visible(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that all major dashboardsections/widgets are visible.
    """
    logged_in_dashboard.verify_all_main_sections_visible()

@pytest.mark.regression
@pytest.mark.dashboard
def test_main_chart_is_visible(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that the main chart in the Published Wafers section is visible.
    """
    logged_in_dashboard.verify_main_chart_visible()

# =========================================================
# Total Published Wafer Count
# =========================================================
@pytest.mark.regression
@pytest.mark.dashboard
def test_total_published_wafer_card_is_visible(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that the Total Published Wafer Count card is visible on the dashboard.
    """
    logged_in_dashboard.verify_total_published_wafer_card_visible()

@pytest.mark.regression
@pytest.mark.dashboard
def test_total_published_wafer_count_is_visible(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that the Total Published Wafer Count section is visible on the dashboard.
    """
    logged_in_dashboard.verify_total_published_wafer_count_visible()

@pytest.mark.regression
@pytest.mark.dashboard
def test_dashboard_page_contains_numeric_summary_data(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that the dashboard page contains numeric summary data in the Total Published Wafer Count section.
    """
    value = logged_in_dashboard.get_total_published_wafer_count()

    assert value is not None
    assert value.strip() != ""
    assert value.strip().lower() not in ["null", "undefined", "nan", "-"]

    normalized = value.replace(",", "").strip()
    assert normalized.isdigit(), f"Expected numeric value for Total Published Wafer Count, but got '{value}'"

# =========================================================
# My Models Section
# =========================================================
@pytest.mark.regression
@pytest.mark.dashboard
def test_my_models_section_is_visible(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that the My Models section is visible on the dashboard.
    """
    logged_in_dashboard.verify_my_models_sections_visible()

@pytest.mark.regression
@pytest.mark.dashboard
def test_my_models_total_count_is_not_empty(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that the total count in My Models section is not empty and contains numeric data.
    """
    value = logged_in_dashboard.get_my_models_total_count()

    assert value is not None
    assert value.strip() != ""
    normalized = value.replace(",", "").strip()
    assert normalized.isdigit(), f"Expected numeric my models total count, but got '{value}'"

@pytest.mark.regression
@pytest.mark.dashboard
@pytest.mark.parametrize(
    "getter_name",
    [
        "get_active_models_count",
        "get_inactive_models_count",
        "get_failed_models_count",
        "get_others_models_count",
    ],
)
def test_each_model_status_count_is_numeric(
    logged_in_dashboard: DashboardPage,
    getter_name: str,
) -> None:
    """
    Verify that each model status count in My Models section contains numeric data.
    """
    getter = getattr(logged_in_dashboard, getter_name)
    value = getter()

    assert value is not None
    assert value.strip() != ""
    normalized = value.replace(",", "").strip()
    assert normalized.isdigit(), f"Expected numeric value from {getter_name}, but got '{value}'"

# =========================================================
# Recently Viewed Models
# =========================================================
@pytest.mark.regression
@pytest.mark.dashboard
def test_recently_viewed_models_section_is_visible(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that the Recently Viewed Models section is visible on the dashboard.
    """
    logged_in_dashboard.verify_recently_viewed_models_section_visible()

@pytest.mark.regression
@pytest.mark.dashboard
def test_recently_viewed_models_empty_state_is_visible_if_applicable(
    logged_in_dashboard: DashboardPage,
) -> None:
    """
    Verify that the empty state for Recently Viewed Models is visible when applicable.
    This test assumes the current test account has no recently viewed models.
    If the account later has recent models, this test may need to be updated.
    """
    logged_in_dashboard.verify_recently_viewed_models_empty_state()

# =========================================================
# Published Wafers / Created Models Chart Sections
# =========================================================
@pytest.mark.regression
@pytest.mark.dashboard
def test_chart_section_controls_are_visible(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that the chart section controls (tabs, dropdowns) are visible in both Published Wafers and Created Models sections.
    """
    logged_in_dashboard.verify_chart_selections_visible()

@pytest.mark.regression
@pytest.mark.dashboard
def test_published_wafers_tabs_are_clickable(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that the Published Wafers section tabs are clickable and that the chart updates accordingly.
    """
    expect(logged_in_dashboard.published_wafers_monthly_tab).to_be_visible()
    expect(logged_in_dashboard.published_wafers_weekly_tab).to_be_visible()

    logged_in_dashboard.click_published_wafers_monthly()
    logged_in_dashboard.wait_for_dashboard_refresh()
    expect(logged_in_dashboard.published_wafers_chart_container).to_be_visible()

    logged_in_dashboard.click_published_wafers_weekly()
    logged_in_dashboard.wait_for_dashboard_refresh()
    expect(logged_in_dashboard.published_wafers_chart_container).to_be_visible()

@pytest.mark.regression
@pytest.mark.dashboard
def test_created_models_tabs_are_clickable(logged_in_dashboard: DashboardPage) -> None:
    """
    Verify that the Created Models section tabs are clickable and that the chart updates accordingly.
    """
    expect(logged_in_dashboard.created_models_monthly_tab).to_be_visible()
    expect(logged_in_dashboard.created_models_weekly_tab).to_be_visible()

    logged_in_dashboard.click_created_models_monthly()
    logged_in_dashboard.wait_for_dashboard_refresh()
    expect(logged_in_dashboard.created_models_chart_container).to_be_visible()

    logged_in_dashboard.click_created_models_weekly()
    logged_in_dashboard.wait_for_dashboard_refresh()
    expect(logged_in_dashboard.created_models_chart_container).to_be_visible()

# =========================================================
# My Models Actions
# =========================================================
@pytest.mark.regression
@pytest.mark.dashboard
@pytest.mark.parametrize(
    "click_method_name,row_attr_name",
    [
        ("click_active_models", "active_models_row"),
        ("click_inactive_models", "inactive_models_row"),
        ("click_failed_models", "failed_models_row"),
        ("click_others_models", "others_models_row"),
    ],
)
def test_model_status_buttons_are_clickable(
    logged_in_dashboard: DashboardPage,
    click_method_name: str,
    row_attr_name: str,
) -> None:
    """
    Verify that the buttons for each model status in My Models section are clickable and lead to the expected results.
    """
    row = getattr(logged_in_dashboard, row_attr_name)
    expect(row).to_be_visible()

    click_method = getattr(logged_in_dashboard, click_method_name)
    click_method()

    # Generic post-click stabilization check
    logged_in_dashboard.wait_for_dashboard_refresh()
    expect(logged_in_dashboard.my_models_card).to_be_visible()