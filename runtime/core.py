import sys

from runtime.profiles import (
    create_profile,
    delete_profile,
    list_profiles,
    switch_profile,
    show_profile,
    get_active_profile,
)
from runtime.executor import exec_in_profile, launch_desktop
from runtime.logging import error

VERSION = "4.2.0-dev"


def show_help():
    active = get_active_profile()
    print(f"""RootFaker Runtime v{VERSION}
------------------------------
Active Profile: {active if active else "None"}

Usage:
  rootfaker <command> [options]

Profile Management:
  rootfaker profile create <name> <distro>
  rootfaker profile delete <name>
  rootfaker profile list
  rootfaker profile switch <name>
  rootfaker profile show [name]

Execution:
  rootfaker exec [profile] <command>
  rootfaker desktop [profile]

Diagnostics:
  rootfaker doctor

Other:
  rootfaker --version
  rootfaker help
""")


def resolve_profile_arg(index):
    """
    If argument at position index exists → use it.
    Otherwise fallback to active profile.
    """
    if len(sys.argv) > index:
        return sys.argv[index]

    active = get_active_profile()
    if not active:
        error("No profile specified and no active profile set.")
        sys.exit(1)

    return active


def main():
    if len(sys.argv) == 1:
        show_help()
        return

    cmd = sys.argv[1]

    try:
        if cmd == "--version":
            print(f"RootFaker Runtime v{VERSION}")

        elif cmd == "help":
            show_help()

        elif cmd == "profile":
            if len(sys.argv) < 3:
                error("Profile command requires subcommand.")
                return

            sub = sys.argv[2]

            if sub == "create":
                if len(sys.argv) != 5:
                    error("Usage: rootfaker profile create <name> <distro>")
                    return
                create_profile(sys.argv[3], sys.argv[4])

            elif sub == "delete":
                if len(sys.argv) != 4:
                    error("Usage: rootfaker profile delete <name>")
                    return
                delete_profile(sys.argv[3])

            elif sub == "list":
                list_profiles()

            elif sub == "switch":
                if len(sys.argv) != 4:
                    error("Usage: rootfaker profile switch <name>")
                    return
                switch_profile(sys.argv[3])

            elif sub == "show":
                profile = resolve_profile_arg(3)
                show_profile(profile)

            else:
                error("Invalid profile command.")

        elif cmd == "exec":
            if len(sys.argv) < 3:
                error("Usage: rootfaker exec [profile] <command>")
                return

            # If user gave profile explicitly
            if len(sys.argv) >= 4 and not sys.argv[2].startswith("-"):
                profile = sys.argv[2]
                command = sys.argv[3:]
            else:
                profile = get_active_profile()
                command = sys.argv[2:]

            if not profile:
                error("No profile specified and no active profile set.")
                return

            if not command:
                error("No command specified.")
                return

            exec_in_profile(profile, command)

        elif cmd == "desktop":
            profile = resolve_profile_arg(2)
            launch_desktop(profile)

        else:
            error(f"Unknown command '{cmd}'")

    except Exception as e:
        error(str(e))


if __name__ == "__main__":
    main()
