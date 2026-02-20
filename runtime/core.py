import sys
import traceback

from runtime.exceptions import RootFakerError
from runtime.profiles import (
    create_profile,
    delete_profile,
    list_profiles,
    switch_profile,
    get_active_profile,
    show_profile,
    profile_exists,
)
from runtime.executor import exec_in_profile


VERSION = "4.1.0-beta"


def safe_main():
    try:
        main()
    except RootFakerError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] Aborted.")
        sys.exit(130)
    except Exception:
        print("[FATAL] Unexpected internal error.")
        sys.exit(2)


def main():
    args = sys.argv[1:]

    if not args:
        print("RootFaker Runtime v" + VERSION)
        print("Use: rootfaker help")
        return

    cmd = args[0]

    # ---------------- VERSION ----------------
    if cmd == "--version":
        print("RootFaker Runtime v" + VERSION)
        return

    # ---------------- HELP ----------------
    if cmd == "help":
        print("Commands:")
        print("  rootfaker profile create <name> <distro>")
        print("  rootfaker profile delete <name>")
        print("  rootfaker profile list")
        print("  rootfaker profile switch <name>")
        print("  rootfaker profile show")
        print("  rootfaker exec <profile> <command>")
        print("  rootfaker --version")
        return

    # ---------------- PROFILE ----------------
    if cmd == "profile":
        if len(args) < 2:
            raise RootFakerError("Profile command requires subcommand.")

        sub = args[1]

        if sub == "create":
            if len(args) != 4:
                raise RootFakerError("Usage: rootfaker profile create <name> <distro>")
            create_profile(args[2], args[3])
            print(f"[SUCCESS] Profile '{args[2]}' created.")
            return

        if sub == "delete":
            if len(args) != 3:
                raise RootFakerError("Usage: rootfaker profile delete <name>")
            delete_profile(args[2])
            print(f"[SUCCESS] Profile '{args[2]}' deleted.")
            return

        if sub == "list":
            profiles = list_profiles()
            print("Profiles:")
            for p in profiles:
                print(" ", p)
            return

        if sub == "switch":
            if len(args) != 3:
                raise RootFakerError("Usage: rootfaker profile switch <name>")
            switch_profile(args[2])
            print(f"[SUCCESS] Active profile: {args[2]}")
            return

        if sub == "show":
            profile = get_active_profile()
            if not profile:
                raise RootFakerError("No active profile.")
            data = show_profile(profile)
            print(f"[INFO] Active profile: {data['profile']}")
            print(f"[INFO] Distro: {data['distro']}")
            print(f"[INFO] Home: {data['home']}")
            print(f"[INFO] Workspace: {data['workspace']}")
            return

        raise RootFakerError("Unknown profile subcommand.")

    # ---------------- EXEC ----------------
    if cmd == "exec":
        if len(args) < 3:
            raise RootFakerError("Usage: rootfaker exec <profile> <command>")

        profile = args[1]

        if not profile_exists(profile):
            raise RootFakerError(f"Profile '{profile}' does not exist.")

        command = args[2:]
        exec_in_profile(profile, command)
        return

    raise RootFakerError("Unknown command.")


if __name__ == "__main__":
    safe_main()
