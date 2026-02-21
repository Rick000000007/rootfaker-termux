import os
import json

from runtime.config import load_profile_config
from runtime.logging import info, error

ROOT_DIR = os.path.expanduser("~/.rootfaker")
PROFILES_DIR = os.path.join(ROOT_DIR, "profiles")
ACTIVE_FILE = os.path.join(ROOT_DIR, "active_profile")


def get_active_profile():
    if not os.path.exists(ACTIVE_FILE):
        return None
    with open(ACTIVE_FILE, "r") as f:
        return f.read().strip()


def set_active_profile(name):
    os.makedirs(ROOT_DIR, exist_ok=True)
    with open(ACTIVE_FILE, "w") as f:
        f.write(name)


def create_profile(name, distro):
    profile_path = os.path.join(PROFILES_DIR, name)

    if os.path.exists(profile_path):
        error(f"Profile '{name}' already exists.")
        return

    os.makedirs(profile_path, exist_ok=True)
    os.makedirs(os.path.join(profile_path, "home"), exist_ok=True)
    os.makedirs(os.path.join(profile_path, "workspace"), exist_ok=True)

    config_path = os.path.join(profile_path, "profile.yaml")
    with open(config_path, "w") as f:
        f.write(f"distro: {distro}\n")
        f.write("env: {}\n")
        f.write("mounts: []\n")
        f.write("runtime:\n")
        f.write("  network: true\n")
        f.write("  shared_tmp: true\n")

    info(f"Profile '{name}' created with distro '{distro}'.")


def delete_profile(name):
    profile_path = os.path.join(PROFILES_DIR, name)

    if not os.path.exists(profile_path):
        error(f"Profile '{name}' does not exist.")
        return

    os.system(f"rm -rf '{profile_path}'")

    if get_active_profile() == name:
        os.remove(ACTIVE_FILE)

    info(f"Profile '{name}' deleted.")


def list_profiles():
    if not os.path.exists(PROFILES_DIR):
        print("No profiles found.")
        return

    active = get_active_profile()

    print("Available Profiles:")
    for name in sorted(os.listdir(PROFILES_DIR)):
        marker = " (active)" if name == active else ""
        print(f"  - {name}{marker}")


def switch_profile(name):
    profile_path = os.path.join(PROFILES_DIR, name)

    if not os.path.exists(profile_path):
        error(f"Profile '{name}' does not exist.")
        return

    set_active_profile(name)
    info(f"Active profile: {name}")


def show_profile(name):
    profile_path = os.path.join(PROFILES_DIR, name)

    if not os.path.exists(profile_path):
        error(f"Profile '{name}' does not exist.")
        return

    config = load_profile_config(name)

    home = os.path.join(profile_path, "home")
    workspace = os.path.join(profile_path, "workspace")

    print("Profile Information")
    print("-------------------")
    print(f"Name:      {name}")
    print(f"Distro:    {config.get('distro')}")
    print(f"Home:      {home}")
    print(f"Workspace: {workspace}")
