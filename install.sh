#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "RootFaker Termux Installer"
echo "--------------------------"

if [ -z "$PREFIX" ]; then
  echo "Run inside Termux only."
  exit 1
fi

pkg update -y
pkg install -y proot proot-distro

mkdir -p "$PREFIX/bin"

cp -f bin/sudo "$PREFIX/bin/sudo"
cp -f bin/root "$PREFIX/bin/root"
cp -f bin/rootfaker "$PREFIX/bin/rootfaker"

chmod +x "$PREFIX/bin/sudo"
chmod +x "$PREFIX/bin/root"
chmod +x "$PREFIX/bin/rootfaker"

echo ""
echo "✅ Installed commands:"
echo "  rootfaker"
echo "  sudo"
echo "  root"
echo ""
echo "Now run: rootfaker"
