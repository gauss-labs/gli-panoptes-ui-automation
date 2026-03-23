# Panoptes UI Automation

Practice UI automation framework for Panoptes using Playwright + Pytest.
The framework follows a Page Objective MOdel (POM) structure and supports environment-based configuration and externalized test data.

## Framework Highlights

Key features of this test framework:

- Playwright + Pytest UI automation
- Page Object Model (POM)
- JSON-based test data (externalized and reusable)
- Multi-environment support (--env)
- Reusable and modular pytest fixtures
- Session-scoped login optimization for faster execution
- Modular page components (e.g., filter modal abstraction)
- Data-driven test support
- HTML test reporting + CI-friendly output (JUnit XML)
- Dynamic UI handling (runtime-discovered elements, no hardcoding)

## Test Coverage

Current automated tests:

- Login authentication
- Dashboard UI validation
- Models page functionality
- Search and filtering
- Pagination behavior
- Table interaction and row actions

## Project Structure

```text
panoptes-ui-tests
│
├── pages/ # Page Object Model classes
│ ├── base_page.py
│ ├── login_page.py
│ ├── dashboard_page.py
│ ├── models_page.py
│ └── components/
│ └── filter_modal.py
│
├── tests/ # UI test cases
│ ├── authentication/
│ │ └── test_login.py
│ ├── dashboard/
│ │ └── test_dashboard.py
│ └── models/
│ ├── test_models_page.py
│ └── test_models_filtering.py
│
├── test_data/
│ ├── env_data.json
│ ├── login_data.json
│ ├── model_data.json
│ └── filter_data.json
│
├── utils/
│ ├── data_reader.py
│ └── env_helper.py
│
├── conftest.py # pytest fixtures and browser setup
├── pytest.ini
└── README.md
```

## Installation

pip install -r requirements.txt 

playwright install


## Environment Configuration

Environment settings are stored in:

    test_data/env.json

Example:\
```json
{
  "mothership_dev": {
    "base_url": "https://gli-vm-web.dev.mothership.gausslabs.ai",
    "username": "admin",
    "password": "gausslabs"
  }
}
```

## Test Data Management

Test input data is managed separately under:
test_data/

Examples include:

- Login credentials
- Model search inputs
- Model creation parameters
- Filter values

## Run tests

Run all tests:

    pytest

Run tests for a specific environment:

    pytest --env=mothership_dev

Run only smoke tests:

    pytest -m smoke

Run only Models tests:

    pytest -m models

## Recent Updates
03/23/2026
- Fixed README (formatting issues)
- Added HTML report output
- Removed duplicate + debug methods
- Cleaned up overall structure

    Fixtures (conftest.py):
- Added models_page fixture (login - navigate - wait for load)
- Added filter_modal fixture
- Added model_test_data fixture (JSON-driven)
- Added session-scoped logged_in_page fixture for optimized login

    Overall improvements:
- Better maintainability
- Reduced flakiness risk
- Improved test performance and readability


03/19/2026
- Added env_name to BasePage to support environment-specific test logic
- Refactored page objects and fixtures to pass env_name consistently
- Removed --headed from pytest.ini and settings.json for CI-friendly execution
- Headed mode is now enabled only via CLI when needed for debugging.
- Grouped import statements and sorted them alphabetically within each group


03/18/2026
- Enhance filter modal automation with dynamic selection and improved stability
- Replaced hardcoded filter options with runtime-discovered values
- Added validation for selected filter count and chip area updates
- Added timeout_ms for mitigate flakiness due to slow filter moda rendering


03/16/2026
- Introduced environment-based configuration using env_data.json
- Externalized test data into JSON files
- Refactored Login, Dashboard, and Models tests to remove hardcoded values
- Added reusable logged_in_page fixture
- Improved pagination button detection