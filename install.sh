#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "RootFaker Termux Installer"
echo "--------------------------"

if [ -z "$PREFIX" ]; then
  echo "❌ Run inside Termux only."
  exit 1
fi

# If mirror issues, user must fix
if ! pkg update -y; then
  echo ""
  echo "❌ pkg update failed."
  echo "Fix mirror using: termux-change-repo"
  exit 1
fi

pkg install -y proot proot-distro curl tar

mkdir -p "$PREFIX/bin"

# Install scripts
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
echo "Run: rootfaker"
