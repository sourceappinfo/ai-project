import unittest
from src.training import train_model

class TestTraining(unittest.TestCase):

    def test_train_model(self):
        # Mock training data
        X_train = ["some text", "another text"]
        y_train = [1, 0]
        model = train_model(X_train, y_train)
        
        # Check if model training is successful
        self.assertIsNotNone(model)

if __name__ == '__main__':
    unittest.main()

