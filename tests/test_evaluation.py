import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from unittest.mock import patch
from src.evaluation import evaluate_model

class TestEvaluation(unittest.TestCase):

    @patch('src.evaluation.joblib.load')
    def test_evaluate_model(self, mock_model):
        """Test evaluating the model."""
        model = mock_model.return_value  # Mock model loading
        X_test = ["some test text", "more test text"]
        y_test = [1, 0]
        
        results = evaluate_model(model, X_test, y_test)
        self.assertIsNotNone(results)
        self.assertIn('accuracy', results)
        self.assertIn('f1_score', results)

    def test_evaluate_model_with_none(self):
        """Test handling None values in model or data."""
        results = evaluate_model(None, None, None)
        self.assertIsNone(results, "Results should be None if model or data is invalid.")

if __name__ == '__main__':
    unittest.main()
