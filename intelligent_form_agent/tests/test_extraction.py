import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.extractor import FormExtractor

class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = FormExtractor()
        self.sample_text = """
        Name: John Doe
        Date of Birth: 12/05/1990
        Email: johndoe@example.com
        Phone: 123-456-7890
        Amount: $1,200.50
        """

    def test_basic_extraction(self):
        data = self.extractor.extract_fields(self.sample_text)
        self.assertEqual(data['name'], "John Doe")
        self.assertEqual(data['email'], "johndoe@example.com")
        self.assertEqual(data['amount'], "$1,200.50")
        # Regex date often picks up the first one
        self.assertIn("12/05/1990", data['dob']) 

    def test_synonyms(self):
        text = "Applicant Name: Jane Smith"
        data = self.extractor.extract_fields(text)
        self.assertEqual(data['name'], "Jane Smith")

if __name__ == '__main__':
    unittest.main()
