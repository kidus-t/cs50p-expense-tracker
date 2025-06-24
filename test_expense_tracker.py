import unittest
import datetime
from expense_tracker import Expense, get_monthly_total

class TestExpenseFunctions(unittest.TestCase):
    def test_monthly_total(self):
        expenses = [
            Expense("Food", 50.0, datetime.date(2025, 6, 1), "Groceries"),
            Expense("Gas", 30.0, datetime.date(2025, 6, 15), "Transport"),
            Expense("Rent", 1000.0, datetime.date(2025, 5, 1), "Housing")
        ]
        result = get_monthly_total(expenses, 2025, 6)
        self.assertEqual(result, 80.0)

if __name__ == '__main__':
    unittest.main()