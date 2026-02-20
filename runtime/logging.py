import sys
from datetime import datetime


def info(message):
    print(f"[INFO] {message}")


def success(message):
    print(f"[SUCCESS] {message}")


def warning(message):
    print(f"[WARNING] {message}")


def error(message):
    print(f"[ERROR] {message}", file=sys.stderr)
