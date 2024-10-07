import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from src.training import train_model

class TestTraining(unittest.TestCase):

    def test_train_model(self):
        """Test model training."""
        X_train = ["some text", "another text"]
        y_train = [1, 0]
        model = train_model(X_train, y_train)
        
        self.assertIsNotNone(model, "Model should be successfully trained and not None.")

    def test_train_model_with_empty_data(self):
        """Test handling empty training data."""
        X_train = []
        y_train = []
        model = train_model(X_train, y_train)
        
        self.assertIsNone(model, "Model training should fail with empty data.")

if __name__ == '__main__':
    unittest.main()
