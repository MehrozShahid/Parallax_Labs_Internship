import unittest

from cleaning import (
    remove_html,
    remove_special_chars,
    normalize_whitespace,
    clean_text
)


class TestCleaningFunctions(unittest.TestCase):

    def test_remove_html(self):
        text = "<h1>Hello</h1>"
        expected = "Hello"
        self.assertEqual(remove_html(text), expected)

    def test_remove_special_chars(self):
        text = "Hello!!! @World#"
        expected = "Hello World"
        self.assertEqual(remove_special_chars(text), expected)

    def test_normalize_whitespace(self):
        text = "Hello     World\n\nPython"
        expected = "Hello World Python"
        self.assertEqual(normalize_whitespace(text), expected)

    def test_empty_text(self):
        text = ""
        expected = ""
        self.assertEqual(clean_text(text), expected)

    def test_none_value(self):
        self.assertEqual(clean_text(None), "")

    def test_long_text(self):
        text = "A" * 120000
        cleaned = clean_text(text)
        self.assertTrue(len(cleaned) <= 100000)


if __name__ == "__main__":
    unittest.main()
