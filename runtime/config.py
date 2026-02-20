import os
import yaml

from runtime.utils import PROFILES_DIR
from runtime.exceptions import RootFakerError


# =============================
# Default Profile Configuration
# =============================

DEFAULT_CONFIG = {
    "distro": "debian",
    "env": {},
    "mounts": [],
    "runtime": {
        "shared_tmp": True,
        "network": True,
    },
}


# =============================
# Path Helpers
# =============================

def get_profile_dir(profile):
    return os.path.join(PROFILES_DIR, profile)


def get_config_path(profile):
    return os.path.join(get_profile_dir(profile), "profile.yaml")


# =============================
# Auto-Heal Config (Legacy Aware)
# =============================

def ensure_profile_config(profile):
    profile_dir = get_profile_dir(profile)

    if not os.path.isdir(profile_dir):
        raise RootFakerError(f"Profile '{profile}' does not exist.")

    config_path = get_config_path(profile)

    if not os.path.exists(config_path):

        # Detect legacy v3 distro file
        legacy_distro_file = os.path.join(profile_dir, "distro")

        if os.path.exists(legacy_distro_file):
            with open(legacy_distro_file, "r") as f:
                detected_distro = f.read().strip()
        else:
            detected_distro = DEFAULT_CONFIG["distro"]

        config = DEFAULT_CONFIG.copy()
        config["distro"] = detected_distro

        with open(config_path, "w") as f:
            yaml.safe_dump(config, f)

    return config_path


# =============================
# Load + Validate Config
# =============================

def load_profile_config(profile):
    config_path = get_config_path(profile)

    if not os.path.exists(config_path):
        ensure_profile_config(profile)

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f) or {}
    except Exception as e:
        raise RootFakerError(f"Invalid YAML in profile '{profile}': {e}")

    return validate_and_normalize(profile, config)


# =============================
# Validation Engine
# =============================

def validate_and_normalize(profile, config):
    if not isinstance(config, dict):
        raise RootFakerError("Profile configuration must be a dictionary.")

    # --- DISTRO ---
    distro = config.get("distro", DEFAULT_CONFIG["distro"])
    if not isinstance(distro, str):
        raise RootFakerError("distro must be a string.")

    # --- ENV ---
    env = config.get("env", {})
    if not isinstance(env, dict):
        raise RootFakerError("env must be a dictionary.")

    for key, value in env.items():
        if not isinstance(key, str):
            raise RootFakerError("Environment variable names must be strings.")
        if not isinstance(value, (str, int, float, bool)):
            raise RootFakerError(
                f"Invalid value type for env '{key}'. Must be string/int/float/bool."
            )

    # --- MOUNTS ---
    mounts = config.get("mounts", [])
    if not isinstance(mounts, list):
        raise RootFakerError("mounts must be a list.")

    seen_guests = set()

    for m in mounts:
        if not isinstance(m, dict):
            raise RootFakerError("Each mount must be a dictionary.")

        if "host" not in m or "guest" not in m:
            raise RootFakerError("Each mount must contain 'host' and 'guest'.")

        host = m["host"]
        guest = m["guest"]

        if not isinstance(host, str) or not isinstance(guest, str):
            raise RootFakerError("Mount host and guest must be strings.")

        if not os.path.exists(os.path.expanduser(host)):
            raise RootFakerError(f"Mount host path does not exist: {host}")

        if not guest.startswith("/"):
            raise RootFakerError("Mount guest path must start with '/'.")

        if guest in seen_guests:
            raise RootFakerError(f"Duplicate guest mount detected: {guest}")

        seen_guests.add(guest)

    # --- RUNTIME OPTIONS ---
    runtime = config.get("runtime", DEFAULT_CONFIG["runtime"])
    if not isinstance(runtime, dict):
        raise RootFakerError("runtime must be a dictionary.")

    for key in ["shared_tmp", "network"]:
        if key in runtime and not isinstance(runtime[key], bool):
            raise RootFakerError(f"runtime.{key} must be boolean.")

    return {
        "distro": distro,
        "env": env,
        "mounts": mounts,
        "runtime": {
            "shared_tmp": runtime.get("shared_tmp", True),
            "network": runtime.get("network", True),
        },
    }
