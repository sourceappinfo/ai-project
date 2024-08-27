import unittest
from src.preprocessing import preprocess_text

class TestPreprocessing(unittest.TestCase):

    def test_preprocess_text(self):
        raw_text = "This is a TEST text."
        cleaned_text = preprocess_text(raw_text)
        
        # Check if text processing is correct
        self.assertEqual(cleaned_text, "test text")

if __name__ == '__main__':
    unittest.main()

