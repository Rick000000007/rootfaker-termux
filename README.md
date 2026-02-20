========================================================
RootFaker-Termux 🔥
User-Space Root Environment for Termux
========================================================

RootFaker-Termux is a community-driven runtime tool that
provides a structured Linux root environment inside Termux
— without rooting Android.

It builds on PRoot isolation while adding a profile-based
runtime engine and advanced CLI system.

WARNING:
This project does NOT root Android.
It creates isolated Linux environments inside Termux.


========================================================
FEATURES
========================================================

[RootFS Management]
- Install Linux distros (Debian, Ubuntu, Alpine, Arch, Fedora)
- Login into installed distros
- Safe removal system
- Default distro configuration

[Fake Root System]
- `root` opens the default distro
- `sudo <command>` runs inside the default distro
- Inside distro you operate as root (PRoot environment)

[Backup + Restore]
- Backup installed distros to .tar.gz
- Restore without full reinstallation
- Safe archive handling

[Profile-Based Runtime - v4.x]
- Multiple isolated profiles
- Structured runtime directories
- Start / Stop lifecycle management
- Bind mount system
- Exec command injection system
- Cleanup and diagnostics tools


========================================================
RELEASE CHANNELS
========================================================

[Stable Channel — v3.x]
Recommended for most users.

- Classic architecture
- Menu-driven workflow
- Basic isolation
- Low risk

v3.x receives bug fixes only.


[Beta Channel — v4.x]
Current Version: v4.1.0-beta

Advanced runtime architecture for power users and testers.

- Structured runtime engine
- Profile system
- Mount management
- Extended CLI
- Runtime status & diagnostics
- Cleanup & orphan detection

NOTE:
v4.x is under active development and may introduce
breaking changes.


========================================================
CLI COMMANDS (Core)
========================================================

rootfaker list
rootfaker install <alias>
rootfaker login <alias>
rootfaker remove <alias>
rootfaker show-default
rootfaker default <alias>


========================================================
ADVANCED CLI (v4 Runtime)
========================================================

[Profile Management]

rootfaker profile create <name> --distro <distro>
rootfaker profile list
rootfaker profile delete <name>

[Runtime Control]

rootfaker start <profile>
rootfaker stop <profile>
rootfaker restart <profile>
rootfaker status <profile>

[Mount Management]

rootfaker mount bind <source> <target>
rootfaker mount bind --ro <source> <target>
rootfaker mount list
rootfaker mount remove <target>

[Execute Commands]

rootfaker exec <profile> -- <command>

Example:
rootfaker exec ubuntu -- ls -la /

[Maintenance]

rootfaker cleanup
rootfaker reset --all

WARNING:
reset --all removes all profiles.


========================================================
INSTALLATION
========================================================

One-Line Install (Recommended)

pkg install curl -y
curl -fsSL https://raw.githubusercontent.com/
Rick000000007/rootfaker-termux/main/quick-install.sh | bash


========================================================
SECURITY MODEL
========================================================

- Does NOT provide real Android root
- Runs fully in user-space
- Uses PRoot isolation
- Cannot modify Android kernel
- Cannot escape Android sandbox


========================================================
ROADMAP
========================================================

v4.2  → Stability improvements
v4.5  → Performance tuning
v5.0  → Runtime isolation redesign
v6.0  → Independent runtime engine (beyond PRoot)


========================================================
VISION
========================================================

RootFaker-Termux aims to evolve from a simple fake-root
helper into a structured runtime engine for advanced
Termux users.

The goal is stability, modularity, and controlled isolation
— without requiring device root.

========================================================
