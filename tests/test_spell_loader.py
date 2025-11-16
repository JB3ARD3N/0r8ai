import unittest

from app.core.spell_loader import load_spells, find_spells_dir


class TestSpellLoader(unittest.TestCase):
    def test_load_spells_returns_list(self):
        spells = load_spells()
        self.assertIsInstance(spells, list)

    def test_spells_directory_has_files(self):
        dirpath = find_spells_dir()
        # Expect at least one YAML file in the repository spells/ folder that ships with the repo
        spells = load_spells(dirpath)
        self.assertGreater(len(spells), 0, f"no spells found in {dirpath}")


if __name__ == "__main__":
    unittest.main()
