import unittest

from template import template_substitution

TEMPLATE = """In a {{hole}} in the ground there lived a {{hobbit}}.
Not a nasty damp smelly {{hole}} filled with the ends of worms and things.
Nor yet a dry sandy {{hole}} with nothing in it to sit down on or eat.
It was a {{hobbit}}-{{hole}} and that means comfort."""

REPLACEMENTS = {"hole": "banana", "hobbit": "wolf"}

EXPECTED_RESULT = """In a banana in the ground there lived a wolf.
Not a nasty damp smelly banana filled with the ends of worms and things.
Nor yet a dry sandy banana with nothing in it to sit down on or eat.
It was a wolf-banana and that means comfort."""


class TestTemplateSubstitution(unittest.TestCase):
    def test_template_substitution(self):
        result = template_substitution(TEMPLATE, REPLACEMENTS)
        self.assertEqual(result, EXPECTED_RESULT)


if __name__ == "__main__":
    unittest.main()
