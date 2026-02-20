import os
import shutil
from runtime.utils import PROFILES_DIR, ACTIVE_PROFILE_FILE
from runtime.config import ensure_profile_config, load_profile_config
from runtime.exceptions import RootFakerError


def profile_path(name):
    return os.path.join(PROFILES_DIR, name)


def profile_exists(name):
    return os.path.isdir(profile_path(name))


def create_profile(name, distro):
    if profile_exists(name):
        raise RootFakerError(f"Profile '{name}' already exists.")

    os.makedirs(profile_path(name), exist_ok=True)
    os.makedirs(os.path.join(profile_path(name), "home"), exist_ok=True)
    os.makedirs(os.path.join(profile_path(name), "workspace"), exist_ok=True)

    # Create default profile.yaml
    ensure_profile_config(name)

    # Overwrite distro in config
    config = load_profile_config(name)
    config["distro"] = distro

    config_path = os.path.join(profile_path(name), "profile.yaml")
    import yaml
    with open(config_path, "w") as f:
        yaml.safe_dump(config, f)

    print(f"[SUCCESS] Profile '{name}' created with distro '{distro}'.")


def list_profiles():
    print("Profiles:")
    if not os.path.isdir(PROFILES_DIR):
        return

    for p in os.listdir(PROFILES_DIR):
        if os.path.isdir(os.path.join(PROFILES_DIR, p)):
            print(f"  {p}")


def switch_profile(name):
    if not profile_exists(name):
        raise RootFakerError(f"Profile '{name}' does not exist.")

    with open(ACTIVE_PROFILE_FILE, "w") as f:
        f.write(name)

    print(f"[SUCCESS] Active profile: {name}")


def get_active_profile():
    if not os.path.exists(ACTIVE_PROFILE_FILE):
        return None

    with open(ACTIVE_PROFILE_FILE, "r") as f:
        return f.read().strip()


def show_profile():
    active = get_active_profile()
    if not active:
        print("No active profile.")
        return

    config = load_profile_config(active)

    print(f"[INFO] Active profile: {active}")
    print(f"[INFO] Distro: {config.get('distro')}")
    print(f"[INFO] Home: {os.path.join(PROFILES_DIR, active, 'home')}")
    print(f"[INFO] Workspace: {os.path.join(PROFILES_DIR, active, 'workspace')}")


def delete_profile(name):
    active = get_active_profile()

    if name == active:
        raise RootFakerError("Cannot delete active profile.")

    if not profile_exists(name):
        raise RootFakerError(f"Profile '{name}' does not exist.")

    shutil.rmtree(profile_path(name))
    print(f"[SUCCESS] Profile '{name}' deleted.")
