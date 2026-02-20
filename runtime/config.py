import os
import yaml
from runtime.exceptions import InvalidProfileConfig

def load_profile_config(profile_path):
    config_file = os.path.join(profile_path, "profile.yaml")

    if not os.path.exists(config_file):
        return {}

    try:
        with open(config_file, "r") as f:
            data = yaml.safe_load(f)
            return data or {}
    except Exception as e:
        raise InvalidProfileConfig(f"Invalid profile.yaml: {e}")
