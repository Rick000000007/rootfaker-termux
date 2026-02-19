# RootFaker-Termux 🔥

RootFaker-Termux is a simple community tool for Termux that provides:

- ✅ Fake `sudo`
- ✅ `root` command (login to Linux rootfs)
- ✅ `rootfaker` menu manager
- ✅ Uses official `proot-distro` rootfs sources
- ✅ Backup + Restore support

⚠️ This project does NOT root Android.
It creates a Linux environment inside Termux using PRoot.

---

## Features

### RootFS Management
- Install Linux distros (Debian, Ubuntu, Alpine, Arch, Fedora, etc.)
- Login into installed distros
- Remove distros safely

### Fake Root System
- `root` opens the default distro
- `sudo <command>` runs inside the default distro
- Inside the distro you are already root

### Backup + Restore
- Backup an installed distro to a `.tar.gz`
- Restore later without reinstalling

---

## Install

```bash
pkg update -y
pkg install git -y
git clone https://github.com/Rick000000007/rootfaker-termux
cd rootfaker-termux
bash install.sh
