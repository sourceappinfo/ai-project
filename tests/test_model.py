import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from unittest.mock import patch
from src.model import load_model

class TestModel(unittest.TestCase):

    @patch('src.model.joblib.load')  # Mock joblib.load to avoid actual file loading
    def test_load_model(self, mock_load):
        """Test loading model."""
        mock_load.return_value = "mock_model_object"  # Mock return value
        model_path = "path/to/fake/model.pkl"
        model = load_model(model_path)

        self.assertIsNotNone(model, "Model should not be None if loaded correctly.")
        self.assertEqual(model, "mock_model_object")

    def test_load_model_with_invalid_path(self):
        """Test loading model from an invalid path."""
        model_path = "path/to/invalid/model.pkl"
        model = load_model(model_path)
        self.assertIsNone(model, "Model should be None when loading from an invalid path.")

if __name__ == '__main__':
    unittest.main()
