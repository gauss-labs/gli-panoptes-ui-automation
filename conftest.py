import pytest
from pages.models_page import ModelsPage
from pages.components.filter_modal import FilterModal
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.data_reader import load_json
from utils.env_helper import get_env_config

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="mothership_dev",
        help="Environment to run tests against"
    )

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "viewport": {"width": 1920, "height": 1080},
    }

@pytest.fixture(scope="session")
def env_name(request) -> str:
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def env_config(env_name: str) -> dict:
    return get_env_config(env_name)

@pytest.fixture(scope="session")
def app_url(env_config: dict) -> str:
    return env_config["base_url"]

@pytest.fixture(scope="session")
def login_test_data() -> dict:
    return load_json("login_data.json")

@pytest.fixture(scope="session")
def filter_test_data() -> dict:
    return load_json("filter_data.json")

@pytest.fixture(scope="session")
def model_test_data() -> dict:
    return load_json("model_data.json")

@pytest.fixture
def login_page(page, app_url, env_name) -> LoginPage:
    return LoginPage(page, app_url, env_name)


@pytest.fixture
def dashboard_page(page, app_url, env_name) -> DashboardPage:
    return DashboardPage(page, app_url, env_name)


@pytest.fixture
def models_page(logged_in_page, app_url, env_name) -> ModelsPage:
    mp = ModelsPage(logged_in_page, app_url, env_name)
    mp.left_navigation.go_to_models()
    mp.wait_for_page_to_load()
    return mp


@pytest.fixture
def filter_modal(page) -> FilterModal:
    return FilterModal(page)

@pytest.fixture
def logged_in_page(page, env_config, env_name):
    login_page = LoginPage(page, env_config["base_url"], env_name)
    login_page.navigate()
    login_page.login(env_config["username"], env_config["password"])
    login_page.verify_login_successful()
    return page