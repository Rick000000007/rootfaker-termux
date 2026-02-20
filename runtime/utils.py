import os

# =============================
# Base Paths
# =============================

HOME = os.path.expanduser("~")
ROOTFAKER_HOME = os.path.join(HOME, ".rootfaker")

# For backward compatibility
BASE_DIR = ROOTFAKER_HOME

PROFILES_DIR = os.path.join(ROOTFAKER_HOME, "profiles")
SNAPSHOTS_DIR = os.path.join(ROOTFAKER_HOME, "snapshots")
ACTIVE_PROFILE_FILE = os.path.join(ROOTFAKER_HOME, "active_profile")


# =============================
# Directory Initialization
# =============================

def ensure_dirs():
    os.makedirs(PROFILES_DIR, exist_ok=True)
    os.makedirs(SNAPSHOTS_DIR, exist_ok=True)


# =============================
# Active Profile
# =============================

def get_active_profile():
    if os.path.isfile(ACTIVE_PROFILE_FILE):
        with open(ACTIVE_PROFILE_FILE, "r") as f:
            return f.read().strip()
    return None


# =============================
# Output Helpers
# =============================

def info(msg):
    print(f"[INFO] {msg}")

def success(msg):
    print(f"[SUCCESS] {msg}")

def error(msg):
    print(f"[ERROR] {msg}")
