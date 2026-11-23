"""RPSA Ruff configuration preset."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

try:
  __version__ = version("rpsa-ruff-config")
except PackageNotFoundError:  # pragma: no cover
  __version__ = "0.0.0"

__all__ = ["__version__", "config_path"]


def config_path() -> Path:
  """Return the absolute path to the packaged ``ruff.toml``."""
  return Path(__file__).resolve().parent / "ruff.toml"
