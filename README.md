# 0r8ai – Local Developer Quick-Start

This project implements a minimal CLI and spell loader so you can quickly inspect and execute YAML-based spells from the `spells/` directory.

## Quick Start (Windows PowerShell)

```powershell
# Activate virtualenv (if using the provided venv)
.\venv\Scripts\Activate.ps1

# Install minimal dependencies
python -m pip install -r requirements.txt

# List spells
python app/main.py list-spells
```

## Features Implemented

### Core Components

- `app/core/spell_loader.py` – Loads and parses YAML spell files
- `app/main.py` – CLI with subcommands (list/show/validate/run)
- `app/core/runner.py` – Executes spells with variable substitution
- `requirements.txt` – Dependencies (PyYAML, jsonschema)

### Validation & Quality

- JSON Schema validation (`app/core/spell_schema.json`)
- `jsonschema` support for strict spell validation
- 20 unit tests (all passing)

### CLI Commands

- `list-spells` – List all available spells (with `--json` for machine-readable output)
- `show-spell <file>` – Display spell details (with `--format json|yaml`)
- `validate-spell <file>` – Validate spell syntax
- `run-spell <file>` – Execute a spell (with `--dry-run` to preview actions)

### Runner Features

- Support for `echo`, `set`, and `noop` actions
- Variable substitution using `{variable}` syntax
- Safe execution with dry-run preview mode

## Example Spell

```yaml
name: Example
description: A simple test spell
steps:
  - action: echo
    message: "Hello from spell"
  - action: set
    variable: result
    value: "success"
```

## Running Tests Locally

### Test on Windows

```powershell
$env:PYTHONPATH='C:\Users\JB\0r8ai'
python -m unittest discover -s tests -p "test_*.py" -v
```

### Test on Linux/macOS

```bash
export PYTHONPATH=/path/to/repo
python -m unittest discover -s tests -p "test_*.py" -v
```

## Building Distributable Artifacts

### Build on Windows

```powershell
.\scripts\build.ps1
```

### Build on Linux/macOS

```bash
./scripts/build.sh
```

This creates `dist/orb-dist-<timestamp>.zip` containing the complete project.

## Packaging

The project includes `pyproject.toml` with setuptools configuration. To build wheel and sdist:

```bash
python -m build --sdist --wheel -o dist/
```

This generates:

- `orb-0.1.0.tar.gz` (source distribution)
- `orb-0.1.0-py3-none-any.whl` (wheel package)

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) automatically:

1. Runs all tests on push and pull requests
2. Builds wheel and sdist packages
3. Creates source distribution zip
4. Uploads artifacts for download

## Development

To extend the project, consider:

- Adding new runner actions (HTTP requests, shell commands, etc.)
- Extending the spell schema with additional validation rules
- Adding linting with pre-commit hooks
