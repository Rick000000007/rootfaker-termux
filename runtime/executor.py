import os
import subprocess

from runtime.config import load_profile_config
from runtime.exceptions import RootFakerError
from runtime.logging import info


# ============================================
# DISTRO LIFECYCLE ENGINE (FINAL CORRECT LOGIC)
# ============================================

def is_distro_installed(distro):
    prefix = os.environ.get("PREFIX", "")
    path = os.path.join(
        prefix,
        "var",
        "lib",
        "proot-distro",
        "installed-rootfs",
        distro,
    )
    return os.path.isdir(path)


def ensure_distro_ready(distro):
    """
    Lifecycle logic:
    - If installed → OK
    - If not installed → attempt install
    - If install fails → unsupported distro
    """

    if is_distro_installed(distro):
        return

    info(f"Distro '{distro}' not installed. Installing automatically...")

    result = subprocess.run(
        ["proot-distro", "install", distro]
    )

    if result.returncode != 0:
        raise RootFakerError(
            f"Distro '{distro}' is not supported by proot-distro."
        )


# ============================================
# EXECUTION ENGINE
# ============================================

def exec_in_profile(profile, command):
    config = load_profile_config(profile)
    distro = config["distro"]

    ensure_distro_ready(distro)

    profile_dir = os.path.expanduser(f"~/.rootfaker/profiles/{profile}")
    home_dir = os.path.join(profile_dir, "home")
    workspace_dir = os.path.join(profile_dir, "workspace")

    os.makedirs(home_dir, exist_ok=True)
    os.makedirs(workspace_dir, exist_ok=True)

    bind_args = []

    # Default mounts
    bind_args += ["--bind", f"{home_dir}:/root"]
    bind_args += ["--bind", f"{workspace_dir}:/workspace"]

    # YAML-defined mounts
    for m in config.get("mounts", []):
        host = os.path.expanduser(m["host"])
        guest = m["guest"]
        bind_args += ["--bind", f"{host}:{guest}"]

    # Environment variables
    env_args = []
    for key, value in config.get("env", {}).items():
        env_args += ["--env", f"{key}={value}"]

    cmd = [
        "proot-distro",
        "login",
        distro,
    ] + bind_args + env_args + ["--"] + command

    subprocess.run(cmd)
