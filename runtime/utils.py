import os

# Base runtime directory
BASE_DIR = os.path.expanduser("~/.rootfaker")

# Profiles directory
PROFILES_DIR = os.path.join(BASE_DIR, "profiles")

# Active profile file
ACTIVE_PROFILE_FILE = os.path.join(BASE_DIR, "active_profile")

# Ensure base directories exist
os.makedirs(PROFILES_DIR, exist_ok=True)
