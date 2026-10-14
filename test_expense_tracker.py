
import json
import os
import tempfile
import unittest
from unittest.mock import patch

import expense_tracker


class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.expenses_file = os.path.join(
            self.temp_dir.name,
            "expenses.json"
        )

        patcher = patch(
            "expense_tracker.FILE_NAME",
            self.expenses_file
        )
        patcher.start()

        self.addCleanup(patcher.stop)
        self.addCleanup(self.temp_dir.cleanup)

    def test_load_expenses_when_file_is_missing(self):
        self.assertEqual(expense_tracker.load_expenses(), [])

    def test_save_and_load_expenses(self):
        expenses = [
            {
                "description": "Lunch",
                "category": "Food",
                "amount": 35.50,
                "date": "2026-10-14"
            }
        ]

        expense_tracker.save_expenses(expenses)

        self.assertEqual(expense_tracker.load_expenses(), expenses)

    def test_add_expense(self):
        expenses = []

        with patch(
            "builtins.input",
            side_effect=["Lunch", "Food", "35.50"]
        ), patch("builtins.print"):
            expense_tracker.add_expense(expenses)

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["description"], "Lunch")
        self.assertEqual(expenses[0]["category"], "Food")
        self.assertEqual(expenses[0]["amount"], 35.50)

        with open(self.expenses_file, encoding="utf-8") as file:
            saved_expenses = json.load(file)

        self.assertEqual(saved_expenses, expenses)

    def test_reject_zero_or_negative_amount(self):
        for amount in ("0", "-10"):
            with self.subTest(amount=amount):
                expenses = []

                with patch(
                    "builtins.input",
                    side_effect=["Test expense", "Other", amount]
                ), patch("builtins.print"):
                    expense_tracker.add_expense(expenses)

                self.assertEqual(expenses, [])

    def test_reject_invalid_amount(self):
        expenses = []

        with patch(
            "builtins.input",
            side_effect=["Lunch", "Food", "abc"]
        ), patch("builtins.print"):
            expense_tracker.add_expense(expenses)

        self.assertEqual(expenses, [])


if __name__ == "__main__":
    unittest.main()
