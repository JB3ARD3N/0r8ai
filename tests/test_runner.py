import unittest

from app.core.runner import run_spell


class TestRunner(unittest.TestCase):
    def test_run_echo(self):
        spell = {"name": "S", "steps": [{"action": "echo", "message": "Hello"}]}
        ok, outputs = run_spell(spell)
        self.assertTrue(ok)
        self.assertEqual(outputs, ["Hello"])

    def test_run_dry_run(self):
        spell = {"name": "S", "steps": [{"action": "echo", "message": "Hi"}]}
        ok, outputs = run_spell(spell, dry_run=True)
        self.assertTrue(ok)
        self.assertIn("[dry-run] echo: Hi", outputs)

    def test_invalid_steps(self):
        spell = {"name": "S", "steps": "not-a-list"}
        ok, outputs = run_spell(spell)
        self.assertFalse(ok)
        self.assertIn("'steps' is not a list", outputs)


if __name__ == "__main__":
    unittest.main()
