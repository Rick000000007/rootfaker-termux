#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "RootFaker Runtime Installer"
echo "----------------------------"

PREFIX=${PREFIX:-/data/data/com.termux/files/usr}
BASE_DIR="$HOME/.rootfaker"
PROFILES_DIR="$BASE_DIR/profiles"
RUNTIME_DEST="$PREFIX/lib/rootfaker"
BIN_DEST="$PREFIX/bin"

echo "[*] Updating package lists..."
apt update -y

echo "[*] Installing required system packages..."
apt install -y \
    python \
    proot \
    proot-distro \
    curl \
    tar

echo "[*] Ensuring pip exists..."
python3 -m ensurepip --upgrade 2>/dev/null || true

echo "[*] Installing Python runtime dependencies..."

# Install PyYAML only if missing
python3 -c "import yaml" 2>/dev/null || pip install pyyaml

echo "[*] Creating runtime directories..."
mkdir -p "$RUNTIME_DEST"
mkdir -p "$PROFILES_DIR"

echo "[*] Deploying runtime engine..."
rm -rf "$RUNTIME_DEST/runtime"
cp -r runtime "$RUNTIME_DEST/"

echo "[*] Deploying launcher..."
cp bin/rootfaker "$BIN_DEST/rootfaker"
chmod +x "$BIN_DEST/rootfaker"

hash -r 2>/dev/null || true

echo ""
echo "✅ RootFaker Runtime installed successfully."
echo ""

# Auto-create default profile if none exists
if [ ! -f "$BASE_DIR/active_profile" ]; then
    echo "[*] No active profile detected."
    echo "[*] Installing default distro (debian)..."
    proot-distro install debian || true

    echo "[*] Creating default profile..."
    "$BIN_DEST/rootfaker" profile create default debian || true
    "$BIN_DEST/rootfaker" profile switch default || true

    echo "✔ Default profile 'default' created."
fi

echo ""
echo "Installation complete."
echo "Run: rootfaker --version"
