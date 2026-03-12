import pytest

BASE_URL = "https://gli-vm-web.dev.mothership.gausslabs.ai"

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "viewport": {"width": 1920, "height": 1080},
    }

@pytest.fixture(scope="session")
def app_url():
    return BASE_URL
