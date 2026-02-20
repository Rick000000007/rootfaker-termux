import os
import subprocess
from runtime.utils import (
    PROFILES_DIR,
    ACTIVE_PROFILE_FILE,
    ensure_dirs,
    info,
    success,
    error,
)

# =============================
# Helpers
# =============================

def profile_path(name):
    return os.path.join(PROFILES_DIR, name)

def profile_exists(name):
    return os.path.isdir(profile_path(name))

def get_profile_distro(name):
    distro_file = os.path.join(profile_path(name), "distro")
    if os.path.isfile(distro_file):
        with open(distro_file, "r") as f:
            return f.read().strip()
    return None


# =============================
# Profile Operations
# =============================

def create_profile(name, distro):
    ensure_dirs()

    if profile_exists(name):
        error(f"Profile '{name}' already exists.")
        return

    path = profile_path(name)
    os.makedirs(os.path.join(path, "home"), exist_ok=True)
    os.makedirs(os.path.join(path, "workspace"), exist_ok=True)

    with open(os.path.join(path, "distro"), "w") as f:
        f.write(distro)

    success(f"Profile '{name}' created with distro '{distro}'.")


def list_profiles():
    ensure_dirs()

    print("Profiles:")
    for name in os.listdir(PROFILES_DIR):
        print(f"  {name}")


def switch_profile(name):
    ensure_dirs()

    if not profile_exists(name):
        error(f"Profile '{name}' does not exist.")
        return

    with open(ACTIVE_PROFILE_FILE, "w") as f:
        f.write(name)

    success(f"Active profile: {name}")


def show_profile():
    ensure_dirs()

    if not os.path.isfile(ACTIVE_PROFILE_FILE):
        error("No active profile set.")
        return

    with open(ACTIVE_PROFILE_FILE, "r") as f:
        active = f.read().strip()

    distro = get_profile_distro(active)

    info(f"Active profile: {active}")
    info(f"Distro: {distro}")


def delete_profile(name):
    ensure_dirs()

    if not profile_exists(name):
        error(f"Profile '{name}' does not exist.")
        return

    if os.path.isfile(ACTIVE_PROFILE_FILE):
        with open(ACTIVE_PROFILE_FILE, "r") as f:
            active = f.read().strip()
        if active == name:
            error("Cannot delete active profile. Switch first.")
            return

    subprocess.run(["rm", "-rf", profile_path(name)])
    success(f"Profile '{name}' deleted.")
