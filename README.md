# Panoptes UI Automation

Practice UI automation framework for Panoptes using Playwright + Pytest.

## Tech Stack

- Python
- Playwright
- Pytest
- Page Object Model (POM)

## Test Coverage

Current automated tests:

- Login authentication
- Dashboard UI validation
- Models page filtering
- Pagination behavior

## Project Structure

pages/ → Page Object Model classes  
tests/ → UI test cases  
fixtures/ → pytest fixtures and browser setup  

## Installation

pip install -r requirements.txt
playwright install

## Run tests

pytest --headed