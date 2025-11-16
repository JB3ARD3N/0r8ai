import unittest

from app.core.runner import run_spell


class TestRunnerVars(unittest.TestCase):
    def test_set_and_echo(self):
        spell = {
            "name": "Vars",
            "steps": [
                {"action": "set", "name": "who", "value": "Alice"},
                {"action": "echo", "message": "Hello {who}"},
            ],
        }
        ok, outputs = run_spell(spell)
        self.assertTrue(ok)
        # first output is set confirmation, second is rendered echo
        self.assertIn("set who=Alice", outputs)
        self.assertIn("Hello Alice", outputs)

    def test_missing_variable(self):
        spell = {"name": "Missing", "steps": [{"action": "echo", "message": "X {nope}"}]}
        ok, outputs = run_spell(spell)
        self.assertTrue(ok)
        # missing var renders as empty string
        self.assertIn("X ", outputs)


if __name__ == "__main__":
    unittest.main()
