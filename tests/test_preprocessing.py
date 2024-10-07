import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from src.preprocessing import preprocess_text

class TestPreprocessing(unittest.TestCase):

    def test_preprocess_text(self):
        """Test text preprocessing."""
        raw_text = "This is a TEST text."
        cleaned_text = preprocess_text(raw_text)
        
        expected_result = "test text"  # Adjust based on actual function behavior
        self.assertEqual(cleaned_text, expected_result, "Cleaned text did not match expected result.")

    def test_preprocess_empty_text(self):
        """Test handling of empty text."""
        raw_text = ""
        cleaned_text = preprocess_text(raw_text)
        self.assertEqual(cleaned_text, "", "Preprocessing empty text should return an empty string.")

if __name__ == '__main__':
    unittest.main()
