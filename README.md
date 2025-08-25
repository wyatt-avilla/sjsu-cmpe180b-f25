# Semester Project for CMPE-180B

## Dependencies

Initialize a virtual environment first if needed:

```sh
python -m venv .venv
source ./.venv/bin/activate
```

Then install the dependencies:

```sh
pip install . # install only necessary dependencies
pip install ".[dev]" # install development dependencies (linters, formatters, etc.)
```

Prettier isn't available on PyPi, so use its
[installation instructions](https://prettier.io/docs/install.html) instead.

test change
