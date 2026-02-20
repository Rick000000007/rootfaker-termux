import os
import subprocess

from runtime.config import load_profile_config
from runtime.exceptions import RootFakerError
from runtime.logging import info


def get_rootfs_path(distro):
    prefix = os.environ.get("PREFIX", "")
    return os.path.join(
        prefix,
        "var",
        "lib",
        "proot-distro",
        "installed-rootfs",
        distro,
    )


def is_distro_installed(distro):
    return os.path.isdir(get_rootfs_path(distro))


def ensure_distro_ready(distro):
    if is_distro_installed(distro):
        return

    info(f"Distro '{distro}' not installed. Installing automatically...")
    result = subprocess.run(["proot-distro", "install", distro])
    if result.returncode != 0:
        raise RootFakerError(
            f"Distro '{distro}' is not supported by proot-distro."
        )


def exec_in_profile(profile, command):
    config = load_profile_config(profile)
    distro = config["distro"]

    ensure_distro_ready(distro)

    profile_dir = os.path.expanduser(f"~/.rootfaker/profiles/{profile}")
    home = os.path.join(profile_dir, "home")
    workspace = os.path.join(profile_dir, "workspace")

    os.makedirs(home, exist_ok=True)
    os.makedirs(workspace, exist_ok=True)

    cmd = [
        "proot-distro",
        "login",
    ]

    # Add bind mounts BEFORE distro name
    cmd += ["--bind", f"{home}:/root"]
    cmd += ["--bind", f"{workspace}:/workspace"]

    for m in config.get("mounts", []):
        host = os.path.expanduser(m["host"])
        guest = m["guest"]
        readonly = m.get("readonly", False)

        if readonly:
            cmd += ["--bind", f"{host}:{guest}:ro"]
        else:
            cmd += ["--bind", f"{host}:{guest}"]

    # Now specify distro
    cmd += [distro, "--", "/bin/sh", "-c", " ".join(command)]

    subprocess.run(cmd)
