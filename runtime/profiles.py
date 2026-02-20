import os

from runtime.config import load_profile_config
from runtime.exceptions import RootFakerError

BASE_DIR = os.path.expanduser("~/.rootfaker")
PROFILES_DIR = os.path.join(BASE_DIR, "profiles")
ACTIVE_PROFILE_FILE = os.path.join(BASE_DIR, "active_profile")


def profile_exists(profile):
    return os.path.isdir(os.path.join(PROFILES_DIR, profile))


def create_profile(profile, distro):
    profile_dir = os.path.join(PROFILES_DIR, profile)

    if profile_exists(profile):
        raise RootFakerError(f"Profile '{profile}' already exists.")

    os.makedirs(os.path.join(profile_dir, "home"), exist_ok=True)
    os.makedirs(os.path.join(profile_dir, "workspace"), exist_ok=True)

    config_path = os.path.join(profile_dir, "profile.yaml")

    with open(config_path, "w") as f:
        f.write(
            f"""# RootFaker Profile Configuration

distro: {distro}

env: {{}}

mounts: []

runtime:
  network: true
  shared_tmp: true
"""
        )


def delete_profile(profile):
    profile_dir = os.path.join(PROFILES_DIR, profile)

    if not profile_exists(profile):
        raise RootFakerError(f"Profile '{profile}' does not exist.")

    active = get_active_profile()
    if active == profile:
        raise RootFakerError(
            "Cannot delete active profile. Switch to another profile first."
        )

    import shutil
    shutil.rmtree(profile_dir)


def list_profiles():
    if not os.path.exists(PROFILES_DIR):
        return []

    return sorted(
        [
            name
            for name in os.listdir(PROFILES_DIR)
            if os.path.isdir(os.path.join(PROFILES_DIR, name))
        ]
    )


def switch_profile(profile):
    if not profile_exists(profile):
        raise RootFakerError(f"Profile '{profile}' does not exist.")

    with open(ACTIVE_PROFILE_FILE, "w") as f:
        f.write(profile)


def get_active_profile():
    if not os.path.exists(ACTIVE_PROFILE_FILE):
        return None

    with open(ACTIVE_PROFILE_FILE, "r") as f:
        return f.read().strip()


def show_profile(profile):
    config = load_profile_config(profile)

    profile_dir = os.path.join(PROFILES_DIR, profile)

    home = os.path.join(profile_dir, "home")
    workspace = os.path.join(profile_dir, "workspace")

    return {
        "profile": profile,
        "distro": config["distro"],
        "home": home,
        "workspace": workspace,
    }
