#!/usr/bin/env python3
"""Small CLI for the 0r8ai project.

Currently provides a `list-spells` command that reads YAML files from the
repo `spells/` directory and prints their name/description.
"""
import argparse


def _cmd_list_spells(args):
	# Import here to keep startup cheap until the command is used.
	from app.core.spell_loader import load_spells

	spells = load_spells()
	if not spells:
		print("No spells found in the repository 'spells/' directory.")
		return

	if args.json:
		import json

		out = []
		for s in spells:
			data = s.get("data", {}) or {}
			out.append({"file": s.get("file"), "name": data.get("name") or data.get("title"), "description": data.get("description", "")})
		print(json.dumps(out, indent=2))
		return

	for s in spells:
		data = s.get("data", {}) or {}
		name = data.get("name") or data.get("title") or s.get("file")
		desc = data.get("description", "").strip()
		if desc:
			print(f"- {name}: {desc}")
		else:
			print(f"- {name}")


def _cmd_show_spell(args) -> int:
	"""Show a single spell file. Returns exit code."""
	from app.core.spell_loader import load_spell_file

	try:
		data = load_spell_file(args.file)
	except FileNotFoundError as e:
		print(str(e))
		return 1

	# Choose output format
	fmt = (args.format or "yaml").lower()
	if fmt == "json":
		import json

		print(json.dumps(data, indent=2))
	else:
		import yaml

		print(yaml.safe_dump(data, sort_keys=False))

	return 0


def _cmd_validate_spell(args):
	from app.core.spell_loader import load_spell_file, validate_spell

	try:
		data = load_spell_file(args.file)
	except FileNotFoundError as e:
		print(str(e))
		return 1

	ok, errors = validate_spell(data)
	if ok:
		print(f"VALID: {args.file}")
		return 0
	else:
		print(f"INVALID: {args.file}")
		for e in errors:
			print(f" - {e}")
		return 2


def main():
	parser = argparse.ArgumentParser(prog="0r8ai")
	sub = parser.add_subparsers(dest="command")
	p0 = sub.add_parser("list-spells", help="List available spell YAML files")
	p0.add_argument("--json", action="store_true", help="Output a JSON array of spells")
	p = sub.add_parser("show-spell", help="Print the full YAML for a spell file")
	p.add_argument("file", help="Spell filename (relative to spells/ or absolute path)")
	p.add_argument("--format", choices=["yaml", "json"], help="Output format (yaml|json)")

	p2 = sub.add_parser("validate-spell", help="Validate a spell YAML file")
	p2.add_argument("file", help="Spell filename (relative to spells/ or absolute path)")
	p3 = sub.add_parser("run-spell", help="Run a spell file")
	p3.add_argument("file", help="Spell filename (relative to spells/ or absolute path)")
	p3.add_argument("--dry-run", action="store_true", help="Do not perform side-effects; show actions")

	args = parser.parse_args()
	if args.command == "list-spells":
		_cmd_list_spells(args)
		return
	elif args.command == "show-spell":
		code = _cmd_show_spell(args)
		import sys

		sys.exit(code)
	elif args.command == "validate-spell":
		code = _cmd_validate_spell(args)
		import sys

		sys.exit(code)
	elif args.command == "run-spell":
		code = _cmd_run_spell(args)
		import sys

		sys.exit(code)
	else:
		parser.print_help()


def _cmd_run_spell(args) -> int:
	from app.core.spell_loader import load_spell_file
	from app.core.runner import run_spell

	try:
		data = load_spell_file(args.file)
	except FileNotFoundError as e:
		print(str(e))
		return 1

	ok, outputs = run_spell(data, dry_run=args.dry_run)
	for o in outputs:
		print(o)

	return 0 if ok else 2


if __name__ == "__main__":
	main()

