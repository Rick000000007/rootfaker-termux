import os
import subprocess

from runtime.config import load_profile_config
from runtime.logging import info


PREFIX = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")


def exec_in_profile(profile, command):
    config = load_profile_config(profile)
    distro = config["distro"]

    subprocess.run(
        [
            "proot-distro",
            "login",
            distro,
            "--shared-tmp",
            "--bind", f"{PREFIX}/tmp:/tmp",
            "--",
            *command
        ],
        env=os.environ.copy()
    )


def launch_desktop(profile):
    config = load_profile_config(profile)
    distro = config["distro"]

    info(f"Launching desktop 'xfce' in profile '{profile}'...")

    subprocess.run(
        [
            "proot-distro",
            "login",
            distro,
            "--shared-tmp",
            "--bind", f"{PREFIX}/tmp:/tmp",
            "--",
            "dbus-launch",
            "--exit-with-session",
            "xfce4-session"
        ],
        env=os.environ.copy()
    )
