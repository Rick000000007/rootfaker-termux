import os
from runtime.config import load_profile_config
from runtime.utils import PROFILES_DIR
from runtime.exceptions import RootFakerError


def inspect_profile(profile):
    profile_dir = os.path.join(PROFILES_DIR, profile)

    if not os.path.isdir(profile_dir):
        raise RootFakerError(f"Profile '{profile}' does not exist.")

    config = load_profile_config(profile)

    home_dir = os.path.join(profile_dir, "home")
    workspace_dir = os.path.join(profile_dir, "workspace")

    print("")
    print(f"Profile: {profile}")
    print(f"Distro: {config.get('distro')}")
    print("")

    print("Paths:")
    print(f"  Home: {home_dir}")
    print(f"  Workspace: {workspace_dir}")
    print("")

    # Mounts
    mounts = config.get("mounts", [])
    print("Mounts:")
    if mounts:
        for m in mounts:
            print(f"  {m.get('host')} -> {m.get('guest')}")
    else:
        print("  None")
    print("")

    # Environment
    env = config.get("env", {})
    print("Environment Variables:")
    if env:
        for k, v in env.items():
            print(f"  {k}={v}")
    else:
        print("  None")
    print("")

    # Runtime options
    runtime_opts = config.get("runtime", {})
    print("Runtime Options:")
    for k, v in runtime_opts.items():
        print(f"  {k}: {v}")
    print("")

    # Snapshots
    snapshot_dir = os.path.expanduser(f"~/.rootfaker/snapshots/{profile}")
    if os.path.isdir(snapshot_dir):
        count = len([f for f in os.listdir(snapshot_dir) if f.endswith(".tar.gz")])
        print(f"Snapshots: {count} found")
    else:
        print("Snapshots: None")

    print("")
