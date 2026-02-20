import sys
import os
import shutil

from runtime.profiles import (
    create_profile,
    list_profiles,
    switch_profile,
    show_profile,
    delete_profile,
    profile_exists,
)

from runtime.executor import exec_in_profile
from runtime.snapshots import (
    create_snapshot,
    list_snapshots,
    restore_snapshot,
)

from runtime.utils import (
    get_active_profile,
    success,
    error,
)

VERSION = "4.0.1-alpha"


# =============================
# Doctor Command
# =============================

def doctor():
    print("RootFaker Doctor")
    print("-----------------")

    # Check proot-distro safely
    if shutil.which("proot-distro"):
        success("proot-distro found")
    else:
        error("proot-distro NOT found")

    # Check active profile
    active = get_active_profile()
    if active:
        success(f"Active profile: {active}")
    else:
        error("No active profile set")

    # Check profiles directory
    profiles_dir = os.path.expanduser("~/.rootfaker/profiles")
    if os.path.isdir(profiles_dir):
        success("Profiles directory OK")
    else:
        error("Profiles directory missing")


# =============================
# Help
# =============================

def print_help():
    print(f"RootFaker Runtime v{VERSION}")
    print("")
    print("Usage:")
    print("  rootfaker --version")
    print("  rootfaker doctor")
    print("")
    print("Profile Management:")
    print("  rootfaker profile create <name> <distro>")
    print("  rootfaker profile list")
    print("  rootfaker profile switch <name>")
    print("  rootfaker profile show")
    print("  rootfaker profile delete <name>")
    print("")
    print("Execution:")
    print("  rootfaker exec <profile> <command>")
    print("")
    print("Snapshot Management:")
    print("  rootfaker snapshot create <profile> <name>")
    print("  rootfaker snapshot list <profile>")
    print("  rootfaker snapshot restore <profile> <name>")
    print("")
    print("Examples:")
    print("  rootfaker profile create dev debian")
    print("  rootfaker exec dev whoami")
    print("  rootfaker snapshot create dev base")
    print("")


# =============================
# CLI Dispatcher
# =============================

def main():
    args = sys.argv[1:]

    if not args:
        print_help()
        return

    # Version
    if args[0] in ["--version", "-v"]:
        print(f"RootFaker Runtime v{VERSION}")
        return

    # Doctor
    if args[0] == "doctor":
        doctor()
        return

    # =============================
    # PROFILE COMMANDS
    # =============================

    if args[0] == "profile":
        if len(args) < 2:
            print_help()
            return

        cmd = args[1]

        if cmd == "create":
            if len(args) != 4:
                error("Usage: rootfaker profile create <name> <distro>")
                return
            create_profile(args[2], args[3])

        elif cmd == "list":
            list_profiles()

        elif cmd == "switch":
            if len(args) != 3:
                error("Usage: rootfaker profile switch <name>")
                return
            switch_profile(args[2])

        elif cmd == "show":
            show_profile()

        elif cmd == "delete":
            if len(args) != 3:
                error("Usage: rootfaker profile delete <name>")
                return
            delete_profile(args[2])

        else:
            print_help()

        return

    # =============================
    # EXEC COMMAND
    # =============================

    if args[0] == "exec":
        if len(args) < 3:
            error("Usage: rootfaker exec <profile> <command>")
            return

        profile = args[1]
        command = args[2:]

        if not profile_exists(profile):
            error(f"Profile '{profile}' does not exist.")
            return

        exec_in_profile(profile, command)
        return

    # =============================
    # SNAPSHOT COMMANDS
    # =============================

    if args[0] == "snapshot":
        if len(args) < 3:
            print_help()
            return

        cmd = args[1]
        profile = args[2]

        if not profile_exists(profile):
            error(f"Profile '{profile}' does not exist.")
            return

        if cmd == "create":
            if len(args) != 4:
                error("Usage: rootfaker snapshot create <profile> <name>")
                return
            create_snapshot(profile, args[3])

        elif cmd == "list":
            list_snapshots(profile)

        elif cmd == "restore":
            if len(args) != 4:
                error("Usage: rootfaker snapshot restore <profile> <name>")
                return
            restore_snapshot(profile, args[3])

        else:
            print_help()

        return

    # Unknown command
    print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        sys.exit(0)
    except Exception as e:
        error(f"Unexpected error: {str(e)}")
        sys.exit(1)
