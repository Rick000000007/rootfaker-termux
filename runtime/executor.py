import os
import subprocess
from runtime.utils import PROFILES_DIR
from runtime.exceptions import ProfileNotFound, RuntimeExecutionError
from runtime.logging import info
from runtime.config import load_profile_config


def exec_in_profile(name, command_args):
    profile_path = os.path.join(PROFILES_DIR, name)

    if not os.path.exists(profile_path):
        raise ProfileNotFound(f"Profile '{name}' does not exist.")

    distro_file = os.path.join(profile_path, "distro")

    if not os.path.exists(distro_file):
        raise RuntimeExecutionError("Profile distro file missing.")

    with open(distro_file, "r") as f:
        distro = f.read().strip()

    home_dir = os.path.join(profile_path, "home")
    workspace_dir = os.path.join(profile_path, "workspace")

    # Load profile.yaml
    config = load_profile_config(profile_path)
    env_vars = config.get("env", {})
    mounts = config.get("mounts", [])

    # Auto-install distro if missing
    installed_rootfs = os.path.join(
        os.environ.get("PREFIX", "/data/data/com.termux/files/usr"),
        "var/lib/proot-distro/installed-rootfs",
        distro,
    )

    if not os.path.exists(installed_rootfs):
        info(f"Installing distro '{distro}'...")
        subprocess.run(["proot-distro", "install", distro], check=True)

    # Base proot command
    proot_command = [
        "proot-distro",
        "login",
        distro,
        "--bind",
        f"{home_dir}:/root",
        "--bind",
        f"{workspace_dir}:/workspace",
    ]

    # Inject dynamic mounts
    for mount in mounts:
        if ":" not in mount:
            raise RuntimeExecutionError(
                f"Invalid mount format: '{mount}'. Use host_path:container_path"
            )

        host, container = mount.split(":", 1)

        host = os.path.expanduser(host)

        if not os.path.exists(host):
            raise RuntimeExecutionError(
                f"Host path does not exist: {host}"
            )

        proot_command.extend(["--bind", f"{host}:{container}"])

    # Inject environment variables
    for key, value in env_vars.items():
        proot_command.extend(["--env", f"{key}={value}"])

    proot_command.append("--")
    proot_command.extend(command_args)

    result = subprocess.run(proot_command)

    if result.returncode != 0:
        raise RuntimeExecutionError(
            f"Command exited with code {result.returncode}"
        )
