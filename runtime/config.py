import os
import yaml

from runtime.exceptions import RootFakerError

BASE_DIR = os.path.expanduser("~/.rootfaker")
PROFILES_DIR = os.path.join(BASE_DIR, "profiles")

ALLOWED_TOP_KEYS = {"distro", "env", "mounts", "runtime"}
ALLOWED_RUNTIME_KEYS = {"network", "shared_tmp"}
ALLOWED_MOUNT_KEYS = {"host", "guest", "readonly"}


def get_profile_path(profile):
    return os.path.join(PROFILES_DIR, profile)


def get_profile_config_path(profile):
    return os.path.join(get_profile_path(profile), "profile.yaml")


# ---------------------------
# VALIDATION HELPERS
# ---------------------------

def validate_top_keys(data):
    unknown = set(data.keys()) - ALLOWED_TOP_KEYS
    if unknown:
        raise RootFakerError(
            f"Invalid keys in profile.yaml: {', '.join(unknown)}"
        )


def validate_distro(data):
    if "distro" not in data:
        raise RootFakerError("Missing required field: distro")

    if not isinstance(data["distro"], str):
        raise RootFakerError("Field 'distro' must be a string.")

    if not data["distro"].strip():
        raise RootFakerError("Field 'distro' cannot be empty.")


def validate_env(data):
    env = data.get("env", {})
    if not isinstance(env, dict):
        raise RootFakerError("Field 'env' must be a dictionary.")

    for key, value in env.items():
        if not isinstance(key, str):
            raise RootFakerError("Environment variable keys must be strings.")
        if not isinstance(value, str):
            raise RootFakerError(
                f"Environment variable '{key}' must have string value."
            )


def validate_mounts(data):
    mounts = data.get("mounts", [])
    if not isinstance(mounts, list):
        raise RootFakerError("Field 'mounts' must be a list.")

    for i, m in enumerate(mounts):
        if not isinstance(m, dict):
            raise RootFakerError(f"Mount entry #{i} must be a dictionary.")

        unknown = set(m.keys()) - ALLOWED_MOUNT_KEYS
        if unknown:
            raise RootFakerError(
                f"Invalid mount keys in entry #{i}: {', '.join(unknown)}"
            )

        if "host" not in m or "guest" not in m:
            raise RootFakerError(
                f"Mount entry #{i} must contain 'host' and 'guest'."
            )

        host = m["host"]
        guest = m["guest"]

        if not isinstance(host, str) or not host.strip():
            raise RootFakerError(f"Mount entry #{i} 'host' must be non-empty string.")

        if not isinstance(guest, str) or not guest.strip():
            raise RootFakerError(f"Mount entry #{i} 'guest' must be non-empty string.")

        host_expanded = os.path.expanduser(host)

        # 🔒 Enforce host path must exist
        if not os.path.exists(host_expanded):
            raise RootFakerError(
                f"Mount entry #{i} host path does not exist: {host_expanded}"
            )

        # 🔒 Enforce guest must be absolute path
        if not guest.startswith("/"):
            raise RootFakerError(
                f"Mount entry #{i} guest path must start with '/': {guest}"
            )

        # 🔒 Prevent dangerous mount to root
        if guest == "/":
            raise RootFakerError(
                f"Mount entry #{i} guest path '/' is not allowed."
            )

        readonly = m.get("readonly", False)
        if not isinstance(readonly, bool):
            raise RootFakerError(
                f"Mount entry #{i} 'readonly' must be boolean."
            )


def validate_runtime(data):
    runtime = data.get("runtime", {})

    if not isinstance(runtime, dict):
        raise RootFakerError("Field 'runtime' must be a dictionary.")

    unknown = set(runtime.keys()) - ALLOWED_RUNTIME_KEYS
    if unknown:
        raise RootFakerError(
            f"Invalid runtime keys: {', '.join(unknown)}"
        )

    for key in runtime:
        if not isinstance(runtime[key], bool):
            raise RootFakerError(
                f"Runtime option '{key}' must be boolean."
            )


def validate_profile_config(data):
    if not isinstance(data, dict):
        raise RootFakerError("profile.yaml must be a dictionary.")

    validate_top_keys(data)
    validate_distro(data)
    validate_env(data)
    validate_mounts(data)
    validate_runtime(data)


# ---------------------------
# LOADER
# ---------------------------

def load_profile_config(profile):
    path = get_profile_config_path(profile)

    if not os.path.exists(path):
        raise RootFakerError(
            f"Profile '{profile}' configuration missing."
        )

    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise RootFakerError(
            f"Invalid YAML in profile '{profile}': {e}"
        )

    if data is None:
        raise RootFakerError("profile.yaml cannot be empty.")

    validate_profile_config(data)

    return data
