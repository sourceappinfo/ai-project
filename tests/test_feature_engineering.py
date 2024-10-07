import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from src.feature_engineering import preprocess_text

class TestFeatureEngineering(unittest.TestCase):

    def test_preprocess_text(self):
        """Test text preprocessing."""
        raw_text = "This is some RAW text! With, punctuation."
        processed_text = preprocess_text(raw_text)
        
        expected_result = "this is some raw text with punctuation"  # Adjust based on actual function behavior
        self.assertEqual(processed_text, expected_result, "Processed text did not match expected result.")

    def test_preprocess_empty_text(self):
        """Test handling of empty text."""
        raw_text = ""
        processed_text = preprocess_text(raw_text)
        self.assertEqual(processed_text, "", "Preprocessing empty text should return an empty string.")

if __name__ == '__main__':
    unittest.main()
