import io
import sys
import unittest
from contextlib import redirect_stdout
import pathlib


def _repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


class TestCLI(unittest.TestCase):
    def _run_main_and_capture(self, argv):
        repo_root = str(_repo_root())
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)

        import app.main as mainmod

        old_argv = sys.argv[:]
        sys.argv = ["app.main"] + argv
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                try:
                    mainmod.main()
                except SystemExit as e:
                    return e.code, buf.getvalue()
        finally:
            sys.argv = old_argv

        return 0, buf.getvalue()

    def _write_temp_spell(self, name: str, data: dict) -> pathlib.Path:
        spells_dir = _repo_root() / "spells"
        spells_dir.mkdir(exist_ok=True)
        p = spells_dir / name
        import yaml

        p.write_text(yaml.safe_dump(data))
        return p

    def test_show_spell_default_yaml(self):
        p = self._write_temp_spell("__test_temp_spell.yaml", {"name": "TempSpell", "steps": []})
        try:
            code, out = self._run_main_and_capture(["show-spell", p.name])
            self.assertEqual(code, 0)
            self.assertIn("TempSpell", out)
        finally:
            p.unlink(missing_ok=True)

    def test_show_spell_json(self):
        p = self._write_temp_spell("__test_temp_spell.json.yaml", {"name": "TempSpellJson", "steps": []})
        try:
            code, out = self._run_main_and_capture(["show-spell", p.name, "--format", "json"])
            self.assertEqual(code, 0)
            self.assertTrue(out.strip().startswith("{"))
        finally:
            p.unlink(missing_ok=True)

    def test_validate_spell_valid(self):
        p = self._write_temp_spell("__test_valid_spell.yaml", {"name": "ValidSpell", "steps": []})
        try:
            code, out = self._run_main_and_capture(["validate-spell", p.name])
            self.assertEqual(code, 0)
            self.assertIn("VALID", out)
        finally:
            p.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
