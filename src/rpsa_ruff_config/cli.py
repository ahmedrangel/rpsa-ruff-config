"""Command line interface: ``rpsa-ruff-config path`` and ``rpsa-ruff-config init``."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from . import config_path


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    prog="rpsa-ruff-config", description="RPSA Ruff configuration preset."
  )
  commands = parser.add_subparsers(dest="command", required=True)
  commands.add_parser("path", help="print the path of the packaged ruff.toml")
  init = commands.add_parser("init", help="copy the preset to a ruff.toml file")
  init.add_argument("--output", "-o", default="ruff.toml", help="destination (default: ruff.toml)")
  init.add_argument("--force", "-f", action="store_true", help="overwrite an existing destination")
  return parser


def main(argv: Sequence[str] | None = None) -> int:
  args = build_parser().parse_args(argv)
  if args.command == "path":
    print(config_path())
    return 0
  destination = Path(args.output)
  if destination.exists() and not args.force:
    print(f"{destination} already exists. Use --force to overwrite it.", file=sys.stderr)
    return 1
  content = config_path().read_text(encoding="utf-8")
  destination.write_text(content, encoding="utf-8", newline="\n")
  print(f"Wrote {destination}")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
