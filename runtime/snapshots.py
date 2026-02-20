import os
import tarfile
import shutil
import json
import hashlib
from datetime import datetime

from runtime.utils import PROFILES_DIR, BASE_DIR
from runtime.exceptions import RuntimeExecutionError
from runtime.logging import info, success


RUNTIME_VERSION = "4.0.0-alpha"

SNAPSHOT_DIR = os.path.join(BASE_DIR, "snapshots")


def _profile_path(name):
    return os.path.join(PROFILES_DIR, name)


def _snapshot_profile_dir(name):
    return os.path.join(SNAPSHOT_DIR, name)


def _get_distro(profile_path):
    distro_file = os.path.join(profile_path, "distro")
    if os.path.exists(distro_file):
        with open(distro_file, "r") as f:
            return f.read().strip()
    return "unknown"


def _calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def create_snapshot(profile, snapshot_name):
    profile_path = _profile_path(profile)

    if not os.path.exists(profile_path):
        raise RuntimeExecutionError(f"Profile '{profile}' does not exist.")

    os.makedirs(_snapshot_profile_dir(profile), exist_ok=True)

    snapshot_file = os.path.join(
        _snapshot_profile_dir(profile),
        f"{snapshot_name}.tar.gz"
    )

    meta_file = os.path.join(
        _snapshot_profile_dir(profile),
        f"{snapshot_name}.meta.json"
    )

    info(f"Creating snapshot '{snapshot_name}' for profile '{profile}'...")

    # Create archive
    with tarfile.open(snapshot_file, "w:gz") as tar:
        tar.add(profile_path, arcname=os.path.basename(profile_path))

    size_bytes = os.path.getsize(snapshot_file)
    sha256_hash = _calculate_sha256(snapshot_file)

    metadata = {
        "profile": profile,
        "distro": _get_distro(profile_path),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "runtime_version": RUNTIME_VERSION,
        "size_bytes": size_bytes,
        "sha256": sha256_hash,
    }

    with open(meta_file, "w") as f:
        json.dump(metadata, f, indent=2)

    success(f"Snapshot saved: {snapshot_file}")
    success("Integrity hash (sha256) generated.")


def list_snapshots(profile):
    profile_snap_dir = _snapshot_profile_dir(profile)

    if not os.path.exists(profile_snap_dir):
        print("No snapshots found.")
        return

    tar_files = [
        f for f in os.listdir(profile_snap_dir)
        if f.endswith(".tar.gz")
    ]

    if not tar_files:
        print("No snapshots found.")
        return

    print("Snapshots:")
    for f in tar_files:
        print(f"  {f}")


def restore_snapshot(profile, snapshot_name):
    profile_path = _profile_path(profile)

    snapshot_file = os.path.join(
        _snapshot_profile_dir(profile),
        f"{snapshot_name}.tar.gz"
    )

    meta_file = os.path.join(
        _snapshot_profile_dir(profile),
        f"{snapshot_name}.meta.json"
    )

    if not os.path.exists(snapshot_file):
        raise RuntimeExecutionError("Snapshot archive not found.")

    if not os.path.exists(meta_file):
        raise RuntimeExecutionError("Snapshot metadata missing.")

    # Verify integrity
    info("Verifying snapshot integrity...")
    with open(meta_file, "r") as f:
        metadata = json.load(f)

    expected_hash = metadata.get("sha256")
    current_hash = _calculate_sha256(snapshot_file)

    if expected_hash != current_hash:
        raise RuntimeExecutionError(
            "Integrity check failed! Snapshot may be corrupted."
        )

    success("Integrity verified.")

    info(f"Restoring snapshot '{snapshot_name}'...")

    if os.path.exists(profile_path):
        shutil.rmtree(profile_path)

    with tarfile.open(snapshot_file, "r:gz") as tar:
        tar.extractall(path=PROFILES_DIR)

    success("Snapshot restored successfully.")
