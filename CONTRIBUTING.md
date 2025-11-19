# Contributing

## Dependencies

> [!NOTE]  
> The development environment is structured with
> [`uv`](https://github.com/astral-sh/uv) in mind, but `pip` can also be used.

Initialize a virtual environment first if needed:

```sh
uv venv
source ./.venv/bin/activate
```

Then install the dependencies:

```sh
uv pip install .        # install only necessary dependencies
uv pip install ".[dev]" # install development dependencies (linters, etc.)
```

## CI

For the specific commands being run, examine the
[repo's actions](https://github.com/wyatt-avilla/sjsu-cmpe180b-f25/tree/main/.github/workflows).

### Formatting

| Language | Tool                                               |
| -------- | -------------------------------------------------- |
| Python   | [`ruff`](https://github.com/astral-sh/ruff)        |
| Markdown | [`prettier`](https://github.com/prettier/prettier) |
| Yaml     | [`prettier`](https://github.com/prettier/prettier) |

### Linting

| Language | Tool                                        |
| -------- | ------------------------------------------- |
| Python   | [`ruff`](https://github.com/astral-sh/ruff) |

### Type Checking

| Language | Tool                                     |
| -------- | ---------------------------------------- |
| Python   | [`mypy`](https://github.com/python/mypy) |
