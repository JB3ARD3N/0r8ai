import unittest

from app.core.spell_loader import validate_spell


class TestValidateSpell(unittest.TestCase):
    def test_valid_spell(self):
        data = {"name": "Example", "steps": []}
        ok, errors = validate_spell(data)
        self.assertTrue(ok)
        self.assertEqual(errors, [])

    def test_missing_name(self):
        data = {"steps": []}
        ok, errors = validate_spell(data)
        self.assertFalse(ok)
        self.assertTrue(any("name" in e for e in errors))

    def test_steps_not_list(self):
        data = {"name": "Bad", "steps": "not-a-list"}
        ok, errors = validate_spell(data)
        self.assertFalse(ok)
        self.assertTrue(any("steps" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
