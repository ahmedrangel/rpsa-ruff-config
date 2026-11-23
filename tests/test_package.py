import subprocess
import sys
from pathlib import Path

import pytest

from rpsa_ruff_config import __version__, config_path
from rpsa_ruff_config.cli import main


def test_config_path_points_to_packaged_file() -> None:
  assert config_path().is_file()
  assert config_path().name == "ruff.toml"


def test_version_is_defined() -> None:
  assert __version__


def test_path_command_prints_config_path(capsys: pytest.CaptureFixture[str]) -> None:
  assert main(["path"]) == 0
  assert capsys.readouterr().out.strip() == str(config_path())


def test_init_copies_preset(tmp_path: Path) -> None:
  destination = tmp_path / "ruff.toml"
  assert main(["init", "--output", str(destination)]) == 0
  assert destination.read_text(encoding="utf-8") == config_path().read_text(encoding="utf-8")


def test_init_refuses_to_overwrite(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
  destination = tmp_path / "ruff.toml"
  destination.write_text("keep", encoding="utf-8")
  assert main(["init", "--output", str(destination)]) == 1
  assert destination.read_text(encoding="utf-8") == "keep"
  assert "already exists" in capsys.readouterr().err


def test_init_force_overwrites(tmp_path: Path) -> None:
  destination = tmp_path / "ruff.toml"
  destination.write_text("old", encoding="utf-8")
  assert main(["init", "--output", str(destination), "--force"]) == 0
  assert destination.read_text(encoding="utf-8") == config_path().read_text(encoding="utf-8")


def test_module_entry_point() -> None:
  result = subprocess.run(
    [sys.executable, "-m", "rpsa_ruff_config", "path"], capture_output=True, text=True, check=False
  )
  assert result.returncode == 0
  assert result.stdout.strip() == str(config_path())
