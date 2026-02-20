import sys

from runtime.logging import info, success, error
from runtime.exceptions import RuntimeExecutionError
from runtime.profiles import (
    create_profile,
    list_profiles,
    switch_profile,
    show_profile,
    delete_profile,
)
from runtime.executor import exec_in_profile
from runtime.snapshots import (
    create_snapshot,
    list_snapshots,
    restore_snapshot,
)


VERSION = "4.0.0-alpha"


def print_help():
    print(f"RootFaker Runtime v{VERSION}")
    print("")
    print("Commands:")
    print("  rootfaker --version")
    print("  rootfaker profile create <name> <distro>")
    print("  rootfaker profile list")
    print("  rootfaker profile switch <name>")
    print("  rootfaker profile show")
    print("  rootfaker profile delete <name>")
    print("  rootfaker exec <profile> <command>")
    print("  rootfaker snapshot create <profile> <name>")
    print("  rootfaker snapshot list <profile>")
    print("  rootfaker snapshot restore <profile> <name>")
    print("  rootfaker doctor")


def main():
    args = sys.argv[1:]

    if not args:
        print_help()
        return

    if args[0] == "--version":
        print(f"RootFaker Runtime v{VERSION}")
        return

    try:

        # =============================
        # PROFILE COMMANDS
        # =============================
        if args[0] == "profile":

            if len(args) < 2:
                print_help()
                return

            action = args[1]

            if action == "create" and len(args) == 4:
                create_profile(args[2], args[3])

            elif action == "list":
                list_profiles()

            elif action == "switch" and len(args) == 3:
                switch_profile(args[2])

            elif action == "show":
                show_profile()

            elif action == "delete" and len(args) == 3:
                delete_profile(args[2])

            else:
                print_help()

        # =============================
        # EXEC COMMAND
        # =============================
        elif args[0] == "exec" and len(args) >= 3:
            profile = args[1]
            command = args[2:]
            exec_in_profile(profile, command)

        # =============================
        # SNAPSHOT COMMANDS
        # =============================
        elif args[0] == "snapshot":

            if len(args) < 3:
                print("Usage:")
                print("  rootfaker snapshot create <profile> <name>")
                print("  rootfaker snapshot list <profile>")
                print("  rootfaker snapshot restore <profile> <name>")
                return

            action = args[1]

            if action == "create" and len(args) == 4:
                create_snapshot(args[2], args[3])

            elif action == "list" and len(args) == 3:
                list_snapshots(args[2])

            elif action == "restore" and len(args) == 4:
                restore_snapshot(args[2], args[3])

            else:
                print("Invalid snapshot command.")

        # =============================
        # DOCTOR
        # =============================
        elif args[0] == "doctor":
            from runtime.doctor import run_doctor
            run_doctor()

        else:
            print_help()

    except RuntimeExecutionError as e:
        error(str(e))
        sys.exit(1)

    except Exception as e:
        error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
