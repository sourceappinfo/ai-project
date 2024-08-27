import unittest
from src.model import load_model

class TestModel(unittest.TestCase):

    def test_load_model(self):
        # Mock model path
        model_path = "path/to/fake/model.pkl"
        model = load_model(model_path)
        
        # Check that the model is loaded properly
        self.assertIsNotNone(model)

if __name__ == '__main__':
    unittest.main()

