import sys
from runtime.logging import info, success, error
from runtime.exceptions import RootFakerError
from runtime.profiles import (
    create_profile,
    list_profiles,
    switch_profile,
    show_profile,
    delete_profile,
    profile_exists
)
from runtime.executor import exec_in_profile
from runtime.inspect import inspect_profile


VERSION = "4.1.0-beta"


def show_help():
    print(f"""
RootFaker Runtime v{VERSION}

Commands:

  rootfaker --version
  rootfaker help

  rootfaker profile create <name> <distro>
  rootfaker profile list
  rootfaker profile switch <name>
  rootfaker profile show
  rootfaker profile delete <name>

  rootfaker exec <profile> <command>
  rootfaker inspect <profile>

  rootfaker doctor
""")


def doctor():
    print("RootFaker Doctor")
    print("-----------------")

    try:
        import shutil
        if shutil.which("proot-distro"):
            success("proot-distro found")
        else:
            error("proot-distro not found")
    except Exception as e:
        error(str(e))


def main():
    args = sys.argv[1:]

    if not args:
        show_help()
        return

    try:

        # --------------------------
        # VERSION
        # --------------------------
        if args[0] == "--version":
            print(f"RootFaker Runtime v{VERSION}")
            return

        # --------------------------
        # HELP
        # --------------------------
        if args[0] == "help":
            show_help()
            return

        # --------------------------
        # DOCTOR
        # --------------------------
        if args[0] == "doctor":
            doctor()
            return

        # --------------------------
        # PROFILE COMMANDS
        # --------------------------
        if args[0] == "profile":

            if len(args) < 2:
                error("Usage: rootfaker profile <command>")
                return

            cmd = args[1]

            if cmd == "create" and len(args) == 4:
                create_profile(args[2], args[3])
                return

            if cmd == "list":
                list_profiles()
                return

            if cmd == "switch" and len(args) == 3:
                switch_profile(args[2])
                return

            if cmd == "show":
                show_profile()
                return

            if cmd == "delete" and len(args) == 3:
                delete_profile(args[2])
                return

            error("Invalid profile command")
            return

        # --------------------------
        # EXECUTION
        # --------------------------
        if args[0] == "exec":
            if len(args) < 3:
                error("Usage: rootfaker exec <profile> <command>")
                return

            profile = args[1]
            command = args[2:]

            if not profile_exists(profile):
                raise RootFakerError(f"Profile '{profile}' does not exist.")

            exec_in_profile(profile, command)
            return

        # --------------------------
        # INSPECT
        # --------------------------
        if args[0] == "inspect":
            if len(args) != 2:
                error("Usage: rootfaker inspect <profile>")
                return

            inspect_profile(args[1])
            return

        error("Unknown command")

    except RootFakerError as e:
        error(str(e))
    except Exception as e:
        error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
