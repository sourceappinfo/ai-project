import unittest
from src.data_loader import load_data

class TestDataLoader(unittest.TestCase):

    def test_load_data(self):
        # Mock processed data path
        processed_data_path = "path/to/fake/data.csv"
        X, y = load_data(processed_data_path)
        
        # Test that the data is loaded correctly
        self.assertIsNotNone(X)
        self.assertIsNotNone(y)
        self.assertGreater(len(X), 0)
        self.assertGreater(len(y), 0)

if __name__ == '__main__':
    unittest.main()

