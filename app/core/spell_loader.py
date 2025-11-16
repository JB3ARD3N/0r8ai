from pathlib import Path
from typing import List, Dict, Optional
import yaml


def _default_spells_dir() -> Path:
	"""Return the repository-level `spells/` directory path.

	The package layout is `app/core`, so go up two parents to the repo root.
	"""
	return Path(__file__).resolve().parents[2] / "spells"


def load_spells(spells_dir: Optional[Path] = None) -> List[Dict]:
	"""Load all YAML files from the spells directory.

	Returns a list of dicts: {"file": <filename>, "data": <parsed_yaml>}.
	Malformed files are skipped.
	"""
	spells_dir = Path(spells_dir) if spells_dir else _default_spells_dir()
	if not spells_dir.exists():
		return []

	spells = []
	for path in spells_dir.glob("*.yaml"):
		try:
			with path.open("r", encoding="utf-8") as f:
				data = yaml.safe_load(f) or {}
			spells.append({"file": path.name, "data": data})
		except Exception:
			# Skip files we can't parse
			continue

	return spells


def find_spells_dir() -> Path:
	"""Public helper to get the spells directory used by load_spells()."""
	return _default_spells_dir()


def load_spell_file(path: Path) -> Dict:
	"""Load a single YAML file and return its parsed contents (or {}).

	`path` may be absolute or relative; if relative it is resolved relative to
	the repository root. If the path includes 'spells/', it is used as-is.
	"""
	p = Path(path)
	if not p.is_absolute():
		# If path is already relative to repo root with spells/ prefix, use as-is
		if p.parts and p.parts[0] == "spells":
			p = Path(__file__).resolve().parents[2] / p
		else:
			# Otherwise, assume it's relative to spells/ directory
			p = _default_spells_dir() / p

	if not p.exists():
		raise FileNotFoundError(f"Spell file not found: {p}")

	with p.open("r", encoding="utf-8") as f:
		return yaml.safe_load(f) or {}


from typing import Tuple
from pathlib import Path
import json

try:
	from jsonschema import validate as _jsonschema_validate, ValidationError as _ValidationError
except Exception:
	_jsonschema_validate = None
	_ValidationError = None


def validate_spell(data: Dict) -> Tuple[bool, List[str]]:
	"""Validate a parsed spell dictionary.

	Uses `app/core/spell_schema.json` with `jsonschema` when available.
	Falls back to minimal checks if the package or schema cannot be loaded.

	Returns (is_valid, errors).
	"""
	errors: List[str] = []
	if not isinstance(data, dict):
		errors.append("spell is not a mapping/dictionary")
		return False, errors

	# Prefer schema-based validation when available
	schema_path = Path(__file__).resolve().parents[0] / "spell_schema.json"
	if _jsonschema_validate and schema_path.exists():
		try:
			schema = json.loads(schema_path.read_text(encoding="utf-8"))
			_jsonschema_validate(instance=data, schema=schema)
			return True, []
		except _ValidationError as e:
			errors.append(str(e))
			return False, errors
		except Exception:
			# fallthrough to minimal checks on unexpected failures
			pass

	# Minimal fallback checks
	name = data.get("name") or data.get("title")
	if not name or not isinstance(name, str):
		errors.append("missing or invalid 'name' (string required)")

	steps = data.get("steps")
	if steps is None:
		errors.append("missing 'steps' (list expected)")
	elif not isinstance(steps, list):
		errors.append("'steps' must be a list")

	return (len(errors) == 0), errors

