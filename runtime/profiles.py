import os
from runtime.utils import PROFILES_DIR, ACTIVE_PROFILE_FILE
from runtime.exceptions import ProfileNotFound, RootFakerError
from runtime.logging import success, info


def create_profile(name, distro):
    profile_path = os.path.join(PROFILES_DIR, name)

    if os.path.exists(profile_path):
        raise RootFakerError(f"Profile '{name}' already exists.")

    os.makedirs(os.path.join(profile_path, "home"))
    os.makedirs(os.path.join(profile_path, "workspace"))

    with open(os.path.join(profile_path, "distro"), "w") as f:
        f.write(distro)

    success(f"Profile '{name}' created with distro '{distro}'.")


def list_profiles():
    if not os.path.exists(PROFILES_DIR):
        return []

    return [
        name for name in os.listdir(PROFILES_DIR)
        if os.path.isdir(os.path.join(PROFILES_DIR, name))
    ]


def switch_profile(name):
    profile_path = os.path.join(PROFILES_DIR, name)

    if not os.path.exists(profile_path):
        raise ProfileNotFound(f"Profile '{name}' does not exist.")

    with open(ACTIVE_PROFILE_FILE, "w") as f:
        f.write(name)

    success(f"Active profile: {name}")


def show_profile():
    if not os.path.exists(ACTIVE_PROFILE_FILE):
        raise RootFakerError("No active profile set.")

    with open(ACTIVE_PROFILE_FILE, "r") as f:
        name = f.read().strip()

    profile_path = os.path.join(PROFILES_DIR, name)

    if not os.path.exists(profile_path):
        raise ProfileNotFound(f"Profile '{name}' not found.")

    with open(os.path.join(profile_path, "distro"), "r") as f:
        distro = f.read().strip()

    info(f"Active profile: {name}")
    info(f"Distro: {distro}")

import shutil
from runtime.utils import PROFILES_DIR, ACTIVE_PROFILE_FILE
from runtime.exceptions import RuntimeExecutionError
from runtime.logging import success


def delete_profile(name):
    profile_path = os.path.join(PROFILES_DIR, name)

    if not os.path.exists(profile_path):
        raise RuntimeExecutionError(f"Profile '{name}' does not exist.")

    # Prevent deleting active profile
    if os.path.exists(ACTIVE_PROFILE_FILE):
        with open(ACTIVE_PROFILE_FILE, "r") as f:
            active = f.read().strip()
            if active == name:
                raise RuntimeExecutionError(
                    "Cannot delete active profile. Switch first."
                )

    shutil.rmtree(profile_path)
    success(f"Profile '{name}' deleted.")
