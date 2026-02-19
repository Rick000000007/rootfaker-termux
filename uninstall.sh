#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "RootFaker Termux Uninstaller"
echo "----------------------------"

if [ -z "$PREFIX" ]; then
  echo "❌ Run inside Termux only."
  exit 1
fi

# Remove installed commands
rm -f "$PREFIX/bin/rootfaker"
rm -f "$PREFIX/bin/sudo"
rm -f "$PREFIX/bin/root"

echo "✅ Removed:"
echo "  rootfaker"
echo "  sudo"
echo "  root"
echo ""

echo "⚠️ Note:"
echo "This does NOT remove installed proot-distro rootfs."
echo "To remove a distro run:"
echo "  proot-distro remove debian"
echo ""

echo "✅ Uninstall complete."
