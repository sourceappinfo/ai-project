import unittest
from src.evaluation import evaluate_model

class TestEvaluation(unittest.TestCase):

    def test_evaluate_model(self):
        # Mock model and data
        model = "mock_model"  # You would replace with an actual model object
        X_test = ["some test text", "more test text"]
        y_test = [1, 0]
        
        # This will depend on how your evaluate_model function is structured
        results = evaluate_model(model, X_test, y_test)
        
        # Check if evaluation is successful
        self.assertIsNotNone(results)
        self.assertIn('accuracy', results)
        self.assertIn('f1_score', results)

if __name__ == '__main__':
    unittest.main()

