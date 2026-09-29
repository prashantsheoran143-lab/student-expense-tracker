import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import expense_tracker as app


class ExpenseTrackerTests(unittest.TestCase):

    def test_next_id(self):
        expenses = [{"id": 1}, {"id": 4}, {"id": 2}]
        self.assertEqual(app.next_id(expenses), 5)

    def test_total_expenses(self):
        expenses = [
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 250.50},
        ]
        self.assertEqual(app.total_expenses(expenses), 350.50)

    def test_category_totals(self):
        expenses = [
            {"id": 1, "amount": 100, "category": "Food"},
            {"id": 2, "amount": 200, "category": "Travel"},
            {"id": 3, "amount": 50, "category": "Food"},
        ]
        self.assertEqual(
            app.category_totals(expenses),
            {"Food": 150, "Travel": 200},
        )

    def test_find_expense(self):
        expenses = [{"id": 7, "title": "Books", "amount": 300}]
        self.assertEqual(
            app.find_expense(expenses, "7")["title"],
            "Books",
        )

    def test_missing_expense(self):
        self.assertIsNone(app.find_expense([], "1"))


if __name__ == "__main__":
    unittest.main()
