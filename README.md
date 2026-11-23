# rpsa-ruff-config

RPSA [Ruff](https://docs.astral.sh/ruff/) configuration preset.

## Install

```sh
py -m pip install rpsa-ruff-config
```

The package depends on `ruff`, so it is installed with it.

## Usage

Ruff reads a config file, not a Python module, so the preset is a `ruff.toml` shipped inside the package. There are two ways to use it.

### Copy it into your project (recommended)

```sh
rpsa-ruff-config init
```

This writes a `ruff.toml` in the current directory. Use `--output` to choose another file and `--force` to overwrite an existing one. Re-run it with `--force` to pick up a newer preset.

The copy is portable across machines and operating systems, and you can edit it freely.

### Extend it

```sh
rpsa-ruff-config path
```

Prints the absolute path of the packaged file. Use it in `extend`:

```toml
# pyproject.toml
[tool.ruff]
extend = "/path/printed/by/the/command/ruff.toml"
```

`extend` only accepts paths, and the installed location depends on the virtual environment and operating system. A path committed to the repository will not work for everyone, so this is only useful for local or generated configs.

## What it sets

| Area | Setting |
| --- | --- |
| Indentation | 2 spaces |
| Quotes | double |
| Line length | 100 |
| Trailing commas | not forced (`skip-magic-trailing-comma`) |
| Target version | `py310` |
| Rule sets | `E` `W` `F` `I` `N` `UP` `B` `C4` `SIM` `PIE` `RUF` |

`__init__.py` files may have unused imports, and `tests/**` ignores `B018` and `N802`.

The full file is [`src/rpsa_ruff_config/ruff.toml`](src/rpsa_ruff_config/ruff.toml). Override anything in your own config as usual.

## Development

Requires Python 3.10 or newer.

```sh
py -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
py -m pip install -e . pytest pytest-cov build
py -m pytest                    # tests, run Ruff against fixtures
py -m ruff check                # this repository uses its own preset
py -m ruff format --check
py -m build
```

## Release

Push a `v*` tag. The `release` workflow publishes to PyPI with [trusted publishing](https://docs.pypi.org/trusted-publishers/). Configure the publisher on PyPI first, using workflow `release.yml` and environment `pypi`.

## License

[MIT](LICENSE.md)
