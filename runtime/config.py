import os
import yaml

from runtime.exceptions import RootFakerError

ALLOWED_TOP_KEYS = {
    "distro",
    "env",
    "mounts",
    "runtime",
    "desktop",
}

ALLOWED_RUNTIME_KEYS = {
    "network",
    "shared_tmp",
}

ALLOWED_DESKTOP_KEYS = {
    "type",
}

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
    return os.path.expanduser(f"~/.rootfaker/profiles/{profile}")

def get_config_path(profile):
    return os.path.join(get_profile_dir(profile), "profile.yaml")

def validate_mount(mount):
    if not isinstance(mount, dict):
        raise RootFakerError("Each mount must be a dictionary.")

    required = {"host", "guest"}
    allowed = {"host", "guest", "readonly"}

    if not required.issubset(mount.keys()):
        raise RootFakerError("Mount must contain 'host' and 'guest'.")

    invalid = set(mount.keys()) - allowed
    if invalid:
        raise RootFakerError(f"Invalid mount keys: {', '.join(invalid)}")

def validate_config(config):
    if not isinstance(config, dict):
        raise RootFakerError("profile.yaml must be a dictionary.")

    invalid_keys = set(config.keys()) - ALLOWED_TOP_KEYS
    if invalid_keys:
        raise RootFakerError(
            f"Invalid keys in profile.yaml: {', '.join(invalid_keys)}"
        )

    if "runtime" in config:
        invalid_runtime = set(config["runtime"].keys()) - ALLOWED_RUNTIME_KEYS
        if invalid_runtime:
            raise RootFakerError(
                f"Invalid runtime keys: {', '.join(invalid_runtime)}"
            )

    if "desktop" in config:
        if not isinstance(config["desktop"], dict):
            raise RootFakerError("desktop must be a dictionary.")

        invalid_desktop = set(config["desktop"].keys()) - ALLOWED_DESKTOP_KEYS
        if invalid_desktop:
            raise RootFakerError(
                f"Invalid desktop keys: {', '.join(invalid_desktop)}"
            )

    for mount in config.get("mounts", []):
        validate_mount(mount)

def load_profile_config(profile):
    config_path = get_config_path(profile)

    if not os.path.exists(config_path):
        raise RootFakerError(f"Profile '{profile}' configuration missing.")

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        raise RootFakerError(f"Invalid YAML in profile '{profile}': {e}")

    validate_config(config)

    merged = DEFAULT_CONFIG.copy()
    merged.update(config)

    return merged
