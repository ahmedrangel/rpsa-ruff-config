import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from rpsa_ruff_config import config_path

FIXTURES = Path(__file__).parent / "fixtures"


class Project:
  """Temporary project that extends the packaged preset and runs Ruff on it."""

  def __init__(self, root: Path) -> None:
    self.root = root
    self.config = root / "ruff.toml"
    self.config.write_text(f'extend = "{config_path().as_posix()}"\n', encoding="utf-8")

  def add_fixture(self, name: str, destination: str | None = None) -> Path:
    target = self.root / (destination or name)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(FIXTURES / name, target)
    return target

  def add_source(self, destination: str, source: str) -> Path:
    target = self.root / destination
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding="utf-8", newline="\n")
    return target

  def _ruff(self, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
      [sys.executable, "-m", "ruff", *args],
      cwd=self.root,
      capture_output=True,
      text=True,
      check=False,
    )

  def check(self, path: Path) -> list[str]:
    result = self._ruff(
      "check", "--no-cache", "--output-format", "json", "--config", str(self.config), str(path)
    )
    assert result.returncode in (0, 1), result.stderr
    return sorted(item["code"] for item in json.loads(result.stdout))

  def format_check(self, path: Path) -> bool:
    result = self._ruff("format", "--no-cache", "--check", "--config", str(self.config), str(path))
    assert result.returncode in (0, 1), result.stderr
    return result.returncode == 0

  def format(self, path: Path) -> str:
    result = self._ruff("format", "--no-cache", "--config", str(self.config), str(path))
    assert result.returncode == 0, result.stderr
    return path.read_text(encoding="utf-8")


@pytest.fixture
def project(tmp_path: Path) -> Project:
  return Project(tmp_path)
