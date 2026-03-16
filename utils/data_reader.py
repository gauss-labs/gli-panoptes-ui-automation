import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_DATA_DIR = PROJECT_ROOT / "test_data"

def load_json(file_name: str) -> Any:
    file_path = TEST_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Test data file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)