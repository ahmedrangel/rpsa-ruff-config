"""A module that follows the preset."""

import os
from pathlib import Path


def list_names(directory: Path) -> list[str]:
  return sorted(entry.name for entry in directory.iterdir() if entry.is_file())


def home() -> str:
  return os.environ.get("HOME", "")
