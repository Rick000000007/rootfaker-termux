# RootFaker-Termux 🔥

RootFaker-Termux is a simple **fake sudo + fake root system** for Termux using **proot + proot-distro**.

It does NOT root your Android device.
It gives you a Linux root shell inside a proot container (Debian/Kali/Ubuntu/etc).

---

## Features
- ✅ Fake `sudo` for Termux
- ✅ `root` command (quick root shell)
- ✅ `rootfaker` manager menu
- ✅ Uses official `proot-distro` rootfs sources
- ✅ Works on all architectures automatically

---

## Install

```bash
pkg update -y
pkg install git -y
git clone https://github.com/Rick000000007/rootfaker-termux
cd rootfaker-termux
bash install.sh
