import io
import sys
import unittest
from contextlib import redirect_stdout
import pathlib


def _repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


class TestCLIRun(unittest.TestCase):
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

    def test_run_spell(self):
        p = self._write_temp_spell("__test_run_spell.yaml", {"name": "RunMe", "steps": [{"action": "echo", "message": "X"}]})
        try:
            code, out = self._run_main_and_capture(["run-spell", p.name])
            self.assertEqual(code, 0)
            self.assertIn("X", out)
        finally:
            p.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
