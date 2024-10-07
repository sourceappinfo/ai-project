import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
import os
import sys

# Ensure that the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_loader import load_processed_data

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        """Set up mock data or test files before each test."""
        self.processed_data_path = "path/to/fake/data.csv"
        # Create a temporary CSV file for testing
        with open(self.processed_data_path, 'w') as f:
            f.write("column1,column2\nvalue1,value2")  # Mock CSV content

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.processed_data_path):
            os.remove(self.processed_data_path)  # Remove the test file

    def test_load_processed_data(self):
        """Test loading processed data."""
        data = load_processed_data(self.processed_data_path)
        self.assertIsNotNone(data, "Data should not be None if the file exists.")
        self.assertGreater(len(data), 0, "Data should contain rows.")

    def test_empty_processed_data(self):
        """Test handling an empty data file."""
        with open(self.processed_data_path, 'w') as f:
            f.write("")  # Write an empty file
        data = load_processed_data(self.processed_data_path)
        self.assertEqual(len(data), 0, "Data should be empty when file is empty.")

if __name__ == '__main__':
    unittest.main()
