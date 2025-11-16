# 0r8ai — local developer quick-start

This small helper implements a minimal CLI and spell loader so you can
quickly inspect the `spells/` YAML files included with the repository.

Quick start (Windows PowerShell):

```powershell
# activate virtualenv (if you use the provided venv)
.\venv\Scripts\Activate.ps1

# install minimal dependencies
python -m pip install -r requirements.txt

# list spells
python -m app.main list-spells
```

What I added:
- `app/core/spell_loader.py` — loads YAML files from `spells/`
- `app/main.py` — minimal CLI with `list-spells`
- `requirements.txt` — PyYAML dependency
- `tests/test_spell_loader.py` — a basic unit test

Added since then:
- JSON Schema validation (`app/core/spell_schema.json`) and `jsonschema` support.
- GitHub Actions CI workflow in `.github/workflows/ci.yml` (runs tests).
- `list-spells --json` for machine-readable output.
- `show-spell --format json` and `validate-spell` commands.

Runner:
- `run-spell <file>`: Executes a simple spell. Supports `--dry-run` to show actions without side-effects.

Example spell with `echo` step:

```yaml
name: Example
steps:
	- action: echo
		message: Hello world
```

To run tests locally (PowerShell):
```powershell
$env:PYTHONPATH='C:\Users\JB\0r8ai'; C:/Users/JB/0r8ai/.git/.venv/Scripts/python.exe -m unittest discover -v
```

If you want stricter validation rules, I can extend the JSON Schema or add Pydantic models.

Autobuild (CI artifact)
 - A GitHub Actions job now runs after tests to create a distributable zip of the repository (`dist/orb-dist-<timestamp>.zip`) and uploads it as an artifact named `orb-dist`.
 - You can also create the zip locally with the included script:

PowerShell (Windows):
```powershell
.
\scripts\build.ps1
```

Linux/macOS:
```bash
./scripts/build.sh
```

If you'd like I can:
- run the unit test now
- add richer CLI commands (show a spell, validate schema)
- wire a small CI workflow
