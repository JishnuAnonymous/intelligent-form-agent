import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.qa import QAEcosystem

class TestQA(unittest.TestCase):
    def setUp(self):
        self.qa = QAEcosystem()
        self.context = """
        The applicant wishes to apply for a loan.
        The purpose is to buy a car.
        The loan duration is 5 years.
        """
        self.fields = {'name': 'Alice'}

    def test_field_answering(self):
        ans = self.qa.answer_question("What is the name?", self.context, self.fields)
        self.assertIn("Alice", ans)

    def test_text_retrieval(self):
        ans = self.qa.answer_question("What is the purpose?", self.context, self.fields)
        self.assertIn("buy a car", ans)

if __name__ == '__main__':
    unittest.main()
