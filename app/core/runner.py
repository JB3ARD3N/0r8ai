from typing import Dict, List, Tuple


class _SafeDict(dict):
    """A dict that returns empty string for missing keys when formatting."""

    def __missing__(self, key):
        return ""


def _render_template(template: str, vars: Dict) -> str:
    try:
        return template.format_map(_SafeDict(vars))
    except Exception:
        # If formatting fails, return original template to avoid hard failure
        return template


def run_spell(spell: Dict, dry_run: bool = False) -> Tuple[bool, List[str]]:
    """Run a simple spell structure.

    Supported step format: list of mappings with an `action` key.
    Supported actions:
    - `echo`: prints `message` (string) with template formatting using variables
    - `set`: sets a variable name to a value (value may be templated)
    - `noop`: does nothing

    Variables set with `set` are available to later steps.

    Returns (success, outputs) where outputs is a list of printed lines.
    """
    outputs: List[str] = []
    vars: Dict = {}

    steps = spell.get("steps") or []
    if not isinstance(steps, list):
        return False, ["'steps' is not a list"]

    for idx, step in enumerate(steps):
        if not isinstance(step, dict):
            outputs.append(f"step {idx}: invalid step (not mapping)")
            continue

        action = step.get("action")
        if action == "echo":
            raw = step.get("message", "")
            rendered = _render_template(str(raw), vars)
            if dry_run:
                outputs.append(f"[dry-run] echo: {rendered}")
            else:
                outputs.append(rendered)
        elif action == "set":
            # set: {"action": "set", "name": "x", "value": "..."}
            name = step.get("name")
            value = step.get("value", "")
            if not name:
                outputs.append(f"step {idx}: set missing 'name'")
                continue
            rendered = _render_template(str(value), vars)
            vars[name] = rendered
            outputs.append(f"set {name}={rendered}")
        elif action == "noop" or action is None:
            outputs.append(f"step {idx}: noop")
        else:
            outputs.append(f"step {idx}: unknown action '{action}'")

    return True, outputs
