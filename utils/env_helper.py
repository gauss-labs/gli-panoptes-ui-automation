from typing import Dict, Any
from utils.data_reader import load_json

def get_env_config(env_name: str) -> Dict[str, Any]:
    env_data = load_json("env_data.json")

    if env_name not in env_data:
        raise ValueError(
            f"Unknown environment: '{env_name}'. "
            f"Available environments: {', '.join(env_data.keys())}"
        )

    return env_data[env_name]