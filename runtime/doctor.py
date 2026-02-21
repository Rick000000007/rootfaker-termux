import shutil
import os
import json

from runtime.profiles import get_active_profile
from runtime.config import load_profile_config
from runtime.exceptions import RootFakerError


def command_exists(cmd):
    return shutil.which(cmd) is not None


def run_doctor(json_mode=False):
    system_checks = {
        "python": command_exists("python3"),
        "proot": command_exists("proot"),
        "proot_distro": command_exists("proot-distro"),
    }

    active_profile = get_active_profile()

    profile_checks = {
        "active": active_profile,
        "yaml_valid": False,
        "distro_installed": False,
    }

    if active_profile:
        try:
            config = load_profile_config(active_profile)
            profile_checks["yaml_valid"] = True

            distro = config.get("distro")
            if distro:
                prefix = os.environ.get("PREFIX", "")
                rootfs_path = os.path.join(
                    prefix,
                    "var",
                    "lib",
                    "proot-distro",
                    "installed-rootfs",
                    distro,
                )
                profile_checks["distro_installed"] = os.path.isdir(rootfs_path)

        except Exception:
            profile_checks["yaml_valid"] = False

    # JSON MODE
    if json_mode:
        output = {
            "api_version": 1,
            "success": True,
            "data": {
                "system": system_checks,
                "profile": profile_checks,
            }
        }
        print(json.dumps(output))
        return

    # CLI MODE
    print("RootFaker Doctor")
    print("-----------------\n")

    print("[System]")
    for key, value in system_checks.items():
        status = "OK" if value else "FAIL"
        print(f"[{status}] {key} found")

    print("\n[Profile]")

    if active_profile:
        print(f"[OK] Active profile: {active_profile}")
    else:
        print("[FAIL] No active profile")

    if profile_checks["yaml_valid"]:
        print("[OK] profile.yaml valid")
    else:
        print("[FAIL] profile.yaml invalid")

    if profile_checks["distro_installed"]:
        print("[OK] Distro installed")
    else:
        print("[FAIL] Distro not installed")

    print("\nDoctor check complete.")
