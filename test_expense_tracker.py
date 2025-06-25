import os
import json
import pytest
from expense_tracker import ExpenseTrackerApp

@pytest.fixture
def app():
    app = ExpenseTrackerApp()
    app.expenses = []
    yield app
    if os.path.exists("expenses.json"):
        os.remove("expenses.json")

def test_add_expense(app):
    app.add_expense("Food", 10.0, "2025-06-25")
    assert len(app.expenses) == 1
    assert app.expenses[0]["category"] == "Food"

def test_save_and_load_expenses(app):
    app.add_expense("Bills", 50.0, "2025-06-24")
    app.save_expenses()
    app.expenses = []
    app.expenses = app.load_expenses()
    assert app.expenses[0]["category"] == "Bills"

def test_get_expense_summary(app):
    app.expenses = [
        {"category": "Food", "amount": 20.0, "date": "2025-06-24"},
        {"category": "Food", "amount": 30.0, "date": "2025-06-25"},
        {"category": "Transport", "amount": 15.0, "date": "2025-06-25"},
    ]
    summary = app.get_expense_summary()
    assert summary["Food"] == 50.0
    assert summary["Transport"] == 15.0
