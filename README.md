# CLI for Data Management

This is simple command line interface for managing data. The idea is that you you write a configuration file in TOML format, and the CLI will take care of the rest (i.e downloading and processing the data).

## Installation

You can install the tool with pip (or another package manager that work with `pyproject.toml` like `uv`), e.g clone the repository and do
```
python3 -m pip install .
```
in the root of the repository.

## Usage

Once installed, you can use the CLI by running the following command:

```bash
dggs-cli /path/to/config.toml
```
or with

```bash
python3 -m dggs_cli /path/to/config.toml
```

Check out the [examples folder](examples) for a more concrete example.

## Contributing
Please install the [pre-commit](https://pre-commit.com/) hooks for linting and formatting.

```bash
python3 -m pip install pre-commit
pre-commit install
```

Open a pull request to contribute changes.

## License
MIT
