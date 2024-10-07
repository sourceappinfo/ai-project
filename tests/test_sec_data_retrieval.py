import unittest
from src.data_loader import fetch_filing_history

class TestSECFilingHistory(unittest.TestCase):

    def test_fetch_filing_history(self):
        """Test fetching filing history for a valid CIK."""
        cik = '0000320193'  # Apple Inc. CIK
        filing_history = fetch_filing_history(cik)
        
        # Ensure we get a response
        self.assertIsNotNone(filing_history, "Filing history should not be None.")
        
        # Check if 'filings' is part of the response
        self.assertIn('filings', filing_history, "'filings' should be in the response JSON.")
        self.assertIn('recent', filing_history['filings'], "'recent' should be in the filings data.")
        
        # Check that recent filings contain entries
        self.assertGreater(len(filing_history['filings']['recent']['form']), 0, "There should be recent filings available.")

if __name__ == '__main__':
    unittest.main()

