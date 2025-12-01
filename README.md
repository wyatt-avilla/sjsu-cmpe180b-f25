# Semester Project for CMPE-180B

![Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fwyatt-avilla%2Fsjsu-cmpe180b-f25%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&logo=python&logoColor=%23F6C83C&label=Python&color=blue)
![Ruff](https://img.shields.io/badge/Ruff-Check-34223D?logo=ruff)
![MyPy](https://img.shields.io/badge/Mypy-Check-blue?logo=python)
![Pytest](https://img.shields.io/github/actions/workflow/status/wyatt-avilla/sjsu-cmpe180b-f25/pytest.yml?logo=pytest&label=Pytest)
![Nix Flake](https://img.shields.io/badge/Nix_Flake-_?logo=nixos&logoColor=CAD3F5&labelColor=grey&color=9173ff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

## Project Setup

For development environment setup instructions see
[Contributing](/CONTRIBUTING.md).

## Execution Instructions

### With `uv`

Inside the cloned repo, run:

```sh
uv run app
```

### With `pip` and `venv`

Inside the cloned repo, run:

```sh
python -m venv .venv
source .venv/bin/activate
pip install .
python -m sjsu_cmpe180b_f25.main
```

### With Nix

Inside the cloned repo, run:

```sh
nix run
```

or, run from the GitHub URL directly with:

```sh
nix run github:wyatt-avilla/sjsu-cmpe180b-f25
```
