import unittest
from src.feature_engineering import preprocess_text

class TestFeatureEngineering(unittest.TestCase):

    def test_preprocess_text(self):
        raw_text = "This is some RAW text! With, punctuation."
        processed_text = preprocess_text(raw_text)
        
        # Test if text is properly processed
        self.assertEqual(processed_text, "raw text punctuation")

if __name__ == '__main__':
    unittest.main()

