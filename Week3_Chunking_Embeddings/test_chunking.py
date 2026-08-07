import unittest

from chunking import split_text


class TestChunking(unittest.TestCase):

    # Check that an empty string returns no chunks
    def test_empty_text(self):
        text = ""
        expected = []
        self.assertEqual(split_text(text), expected)

    # Check that None is handled safely
    def test_none_value(self):
        self.assertEqual(split_text(None), [])

    # Small text should stay as one chunk
    def test_short_text(self):
        text = "Hello World"
        chunks = split_text(text)
        self.assertEqual(len(chunks), 1)

    # Long text should be divided into multiple chunks
    def test_long_text(self):
        text = "Artificial Intelligence " * 500
        chunks = split_text(text)
        self.assertTrue(len(chunks) > 1)

    # The splitter should still work even if there are no full stops
    def test_text_without_sentences(self):
        text = "machinelearning " * 500
        chunks = split_text(text)
        self.assertTrue(len(chunks) > 1)


if __name__ == "__main__":
    unittest.main()