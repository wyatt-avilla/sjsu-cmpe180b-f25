# Semester Project for CMPE-180B

![Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fwyatt-avilla%2Fsjsu-cmpe180b-f25%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&logo=python&logoColor=%23F6C83C&label=Python&color=blue)
![Ruff](https://img.shields.io/badge/Ruff-Check-34223D?logo=ruff)
[![MyPy](https://img.shields.io/badge/Mypy-Check-blue?logo=python)](https://github.com/wyatt-avilla/sjsu-cmpe180b-f25/actions/workflows/type-checking.yml)
[![Pytest](https://img.shields.io/github/actions/workflow/status/wyatt-avilla/sjsu-cmpe180b-f25/pytest.yml?logo=pytest&label=Pytest)](https://github.com/wyatt-avilla/sjsu-cmpe180b-f25/actions/workflows/pytest.yml)
![Nix Flake](https://img.shields.io/badge/Nix_Flake-_?logo=nixos&logoColor=CAD3F5&labelColor=grey&color=9173ff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

## Project Setup

For development environment setup instructions see
[Contributing](/CONTRIBUTING.md).

## Execution Instructions

The following command line options are available:

```txt
uv run app --help
usage: app [-h] [--database-url DATABASE_URL] [--populate-db]
           [--log-level {critical,error,warning,info,debug}] [--request-loan COPY_ID MEMBER_ID]
           [--end-loan LOAN_ID] [--pay-fine FINE_ID] [--top-books N] [--overdue-members]
           [--unpaid-fines-members AMOUNT] [--copies-on-loans N] [--genre-fine-stats]
           [--create-indexes] [--drop-indexes]
           [--explain {top_books,overdue_members,unpaid_fines}]

CMPE-180b Project Command Line Interface

options:
  -h, --help            show this help message and exit
  --database-url DATABASE_URL
                        URL for the database. Takes priority over the `DATABASE_URL` environment
                        variable. Required if DATABASE_URL is not set.
  --populate-db         Populate the database with initial data.
  --log-level {critical,error,warning,info,debug}
                        Logging verbosity. Defaults to info.
  --request-loan COPY_ID MEMBER_ID
                        Create a new loan for the specified copy ID and member ID.
  --end-loan LOAN_ID    End the loan with the specified loan ID.
  --pay-fine FINE_ID    Pay the fine with the specified ID.
  --top-books N         Show the top N most loaned books.
  --overdue-members     List members who currently have overdue loans.
  --unpaid-fines-members AMOUNT
                        List members whose unpaid fines total with optional minimum amount.
  --copies-on-loans N   Show the top N books based on copies on loans.
  --genre-fine-stats    Show fine statistics grouped by book genre.
  --create-indexes      Create indexes that optimize the complex queries.
  --drop-indexes        Drop all created indexes.
  --explain {top_books,overdue_members,unpaid_fines}
                        Run EXPLAIN ANALYZE on a complex query.
```

### Running With `uv`

Inside the cloned repo, run:

```sh
uv run app
```

### Running With `pip` and `venv`

Inside the cloned repo, run:

```sh
python -m venv .venv
source .venv/bin/activate
pip install .
python -m sjsu_cmpe180b_f25.main
```

### Running With Nix

Inside the cloned repo, run:

```sh
nix run
```

or, run from the GitHub URL directly with:

```sh
nix run github:wyatt-avilla/sjsu-cmpe180b-f25
```

## Dependencies

Dependencies are specified in the `[project.dependencies]` table within
[`pyproject.toml`](./pyproject.toml). Locking each dependency to a specific
version is done with `uv lock` and reflected in `uv.lock`.

### Installing Dependencies

Inside the cloned repo, and ideally within a virtual environment run:

```sh
uv pip install .
```

<!-- prettier-ignore-start -->
> [!NOTE]
Remove the `uv` prefix from the previous command to use `pip` instead.
<!-- prettier-ignore-end -->

## Testing

Tests are done with [`pytest`](https://github.com/pytest-dev/pytest). They are
defined in the `tests/` directory and ran on pushes/pull requests to `main`. You
can view the latest status
[here](https://github.com/wyatt-avilla/sjsu-cmpe180b-f25/actions/workflows/pytest.yml).
