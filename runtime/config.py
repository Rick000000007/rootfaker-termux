import os
import yaml

from runtime.exceptions import RootFakerError

ROOTFAKER_HOME = os.path.expanduser("~/.rootfaker")
PROFILES_DIR = os.path.join(ROOTFAKER_HOME, "profiles")

DEFAULT_CONFIG = {
    "distro": "debian",
    "env": {},
    "mounts": [],
    "runtime": {
        "network": True,
        "shared_tmp": True,
    },
}


def get_profile_dir(profile):
    return os.path.join(PROFILES_DIR, profile)


def get_config_path(profile):
    return os.path.join(get_profile_dir(profile), "profile.yaml")


def ensure_profile_config(profile):
    profile_dir = get_profile_dir(profile)

    if not os.path.isdir(profile_dir):
        raise RootFakerError(f"Profile '{profile}' does not exist.")

    config_path = get_config_path(profile)

    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            yaml.safe_dump(DEFAULT_CONFIG, f)

    return config_path


def load_profile_config(profile):
    config_path = ensure_profile_config(profile)

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f) or {}
    except Exception as e:
        raise RootFakerError(
            f"Invalid YAML in profile '{profile}': {e}"
        )

    # merge defaults
    merged = DEFAULT_CONFIG.copy()
    merged.update(config)

    return merged
