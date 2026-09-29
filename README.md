# Student Expense Tracker

A small command-line program I wrote in Python to keep track of my daily spending. It saves everything to a JSON file, so your entries are still there the next time you open it.

## What it does
- Add, view, update and delete expenses
- Search by title, category, date or note
- Eight categories to sort spending into
- Total, average and biggest expense
- Spending broken down by category
- Total for any month, plus a check against a monthly budget

Categories: Food, Travel, Education, Shopping, Entertainment, Bills, Health, Other.

## Built with
Python 3 and nothing else. It only uses `json`, `datetime` and `pathlib` from the standard library, so there is nothing to install.

## Running it
```bash
python expense_tracker.py
```

## Running the tests
```bash
python -m unittest discover -s tests -v
```
