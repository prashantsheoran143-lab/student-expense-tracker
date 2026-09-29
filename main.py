"""
Student Expense Tracker
A beginner-friendly command-line expense management system.
Uses JSON file storage and Python standard library only.
"""

import json
import math
import os
import sys
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "expenses.json"

CATEGORIES = [
    "Food",
    "Travel",
    "Education",
    "Shopping",
    "Entertainment",
    "Bills",
    "Health",
    "Other",
]


def get_currency_symbol():
    """Use ₹ if the terminal can display it, otherwise fall back to 'Rs.'."""
    encoding = getattr(sys.stdout, "encoding", None) or "ascii"
    try:
        "₹".encode(encoding)
        return "₹"
    except (UnicodeEncodeError, LookupError):
        return "Rs."


CUR = get_currency_symbol()


# ---------------------------------------------------------------- storage ---

def clean_record(record):
    """Return a valid expense dict, or None if the record is unusable."""
    if not isinstance(record, dict):
        return None
    try:
        amount = float(record["amount"])
        if not math.isfinite(amount) or amount <= 0:
            return None
        date = datetime.strptime(str(record.get("date", "")), "%Y-%m-%d").strftime("%Y-%m-%d")
        return {
            "id": int(record["id"]),
            "title": str(record.get("title", "Untitled")),
            "amount": round(amount, 2),
            "category": str(record.get("category", "Other")),
            "date": date,
            "note": str(record.get("note", "") or ""),
        }
    except (KeyError, TypeError, ValueError):
        return None


def load_expenses():
    """Load expense records from JSON storage."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        # Keep the unreadable file as a backup so it is never overwritten.
        backup = DATA_FILE.with_suffix(".corrupt.json")
        try:
            os.replace(DATA_FILE, backup)
            print(f"Warning: Could not read expense data. Saved a copy as {backup.name}.")
        except OSError:
            print("Warning: Could not read expense data. Starting with an empty list.")
        return []

    if not isinstance(data, list):
        return []

    expenses, seen_ids = [], set()
    skipped = 0
    for record in data:
        cleaned = clean_record(record)
        if cleaned is None or cleaned["id"] in seen_ids:
            skipped += 1
            continue
        seen_ids.add(cleaned["id"])
        expenses.append(cleaned)

    if skipped:
        print(f"Warning: Skipped {skipped} invalid record(s) in the data file.")
    return expenses


def save_expenses(expenses):
    """Save expense records safely (write to temp file, then replace)."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp_file = DATA_FILE.with_suffix(".tmp")

    with temp_file.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)

    os.replace(temp_file, DATA_FILE)


def next_id(expenses):
    """Return the next available expense ID."""
    return max((expense["id"] for expense in expenses), default=0) + 1


def find_expense(expenses, expense_id):
    """Find an expense by ID."""
    try:
        expense_id = int(expense_id)
    except ValueError:
        return None

    return next((e for e in expenses if e["id"] == expense_id), None)


# ------------------------------------------------------------ input helpers ---

def parse_positive_number(text):
    """Return a positive finite float from text, or None if invalid."""
    try:
        value = float(text)
    except ValueError:
        return None
    if not math.isfinite(value) or value <= 0:
        return None
    return round(value, 2)


def read_amount(prompt=None, current=None):
    """Read a positive amount. If current is given, ENTER keeps it."""
    prompt = prompt or f"Amount ({CUR}): "
    while True:
        text = input(prompt).strip()

        if not text and current is not None:
            return current

        amount = parse_positive_number(text)
        if amount is not None:
            return amount
        print("Please enter a valid number greater than zero.")


def read_date(current=None):
    """Read a date in YYYY-MM-DD format. ENTER uses the default/current."""
    default = current or str(datetime.now().date())
    while True:
        date_text = input(f"Date (YYYY-MM-DD) [{default}]: ").strip()

        if not date_text:
            return default

        try:
            # Normalize so "2026-9-2" is stored as "2026-09-02".
            return datetime.strptime(date_text, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")


def read_month():
    """Read a month in YYYY-MM format, or return None if invalid."""
    month = input("Enter month (YYYY-MM): ").strip()
    try:
        # Normalize so "2026-9" becomes "2026-09".
        return datetime.strptime(month, "%Y-%m").strftime("%Y-%m")
    except ValueError:
        print("Invalid month. Use YYYY-MM.")
        return None


def choose_category(current=None):
    """Display categories and return the selected category."""
    print("\nCategories:")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")

    while True:
        choice = input("Choose category: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]

        # During update, ENTER keeps the existing category.
        if current is not None and choice == "":
            return current

        print("Invalid category. Please choose a number from the list.")


# ---------------------------------------------------------------- features ---

def add_expense(expenses):
    """Create and save a new expense."""
    print("\n--- Add Expense ---")

    title = input("Expense title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    amount = read_amount()
    category = choose_category()
    date = read_date()
    note = input("Note (optional): ").strip()

    expenses.append(
        {
            "id": next_id(expenses),
            "title": title,
            "amount": amount,
            "category": category,
            "date": date,
            "note": note,
        }
    )
    save_expenses(expenses)
    print("Expense added successfully.")


def display_expense(expense):
    """Display one expense record."""
    print(
        f"ID: {expense['id']} | "
        f"{expense['date']} | "
        f"{expense['title']} | "
        f"{CUR}{expense['amount']:.2f} | "
        f"{expense['category']}"
    )
    if expense.get("note"):
        print(f"   Note: {expense['note']}")


def view_expenses(expenses):
    """Display all expense records."""
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded.")
        return

    for expense in sorted(expenses, key=lambda e: (e["date"], e["id"]), reverse=True):
        display_expense(expense)

    print(f"\nTotal records: {len(expenses)}")


def search_expenses(expenses):
    """Search expenses by title, category, date, or note."""
    query = input("Search: ").strip().lower()

    if not query:
        print("Search text cannot be empty.")
        return

    matches = [
        e
        for e in expenses
        if query in e["title"].lower()
        or query in e["category"].lower()
        or query in e["date"].lower()
        or query in e["note"].lower()
    ]

    if not matches:
        print("No matching expenses found.")
        return

    print(f"\nFound {len(matches)} expense(s):")
    for expense in matches:
        display_expense(expense)


def update_expense(expenses):
    """Update an existing expense."""
    expense = find_expense(expenses, input("Enter expense ID to update: ").strip())

    if not expense:
        print("Expense not found.")
        return

    print("Press ENTER to keep the existing value.")

    title = input(f"Title [{expense['title']}]: ").strip()
    if title:
        expense["title"] = title

    expense["amount"] = read_amount(
        f"Amount [{CUR}{expense['amount']:.2f}]: ", current=expense["amount"]
    )
    expense["category"] = choose_category(expense["category"])
    expense["date"] = read_date(current=expense["date"])

    note = input(f"Note [{expense['note']}] (type - to clear): ").strip()
    if note == "-":
        expense["note"] = ""
    elif note:
        expense["note"] = note

    save_expenses(expenses)
    print("Expense updated successfully.")


def delete_expense(expenses):
    """Delete an expense after confirmation."""
    expense = find_expense(expenses, input("Enter expense ID to delete: ").strip())

    if not expense:
        print("Expense not found.")
        return

    confirm = input(
        f"Delete '{expense['title']}' ({CUR}{expense['amount']:.2f})? (y/n): "
    ).strip().lower()

    if confirm == "y":
        expenses.remove(expense)
        save_expenses(expenses)
        print("Expense deleted successfully.")
    else:
        print("Delete cancelled.")


def total_expenses(expenses):
    """Return total amount spent."""
    return round(sum(e["amount"] for e in expenses), 2)


def category_totals(expenses):
    """Return spending totals grouped by category."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return {key: round(value, 2) for key, value in totals.items()}


def spent_in_month(expenses, month):
    """Return total spending for a YYYY-MM month."""
    return round(sum(e["amount"] for e in expenses if e["date"].startswith(month)), 2)


def monthly_total(expenses):
    """Calculate spending for a selected month."""
    month = read_month()
    if month is None:
        return
    print(f"Total spending for {month}: {CUR}{spent_in_month(expenses, month):.2f}")


def show_summary(expenses):
    """Display spending statistics."""
    print("\n--- Expense Summary ---")

    if not expenses:
        print("No expenses available.")
        return

    total = total_expenses(expenses)
    average = total / len(expenses)
    highest = max(expenses, key=lambda e: e["amount"])
    categories = category_totals(expenses)

    print(f"Number of expenses : {len(expenses)}")
    print(f"Total spent        : {CUR}{total:.2f}")
    print(f"Average expense    : {CUR}{average:.2f}")
    print(f"Largest expense    : {highest['title']} ({CUR}{highest['amount']:.2f})")

    print("\nSpending by category:")
    for category, amount in sorted(categories.items(), key=lambda i: i[1], reverse=True):
        print(f"{category:<18}: {CUR}{amount:.2f}")


def show_budget_status(expenses):
    """Compare spending with a user-provided monthly budget."""
    budget = read_amount(f"Enter monthly budget ({CUR}): ")

    month = read_month()
    if month is None:
        return

    spent = spent_in_month(expenses, month)
    remaining = round(budget - spent, 2)

    print(f"\nBudget for {month}: {CUR}{budget:.2f}")
    print(f"Spent             : {CUR}{spent:.2f}")

    if remaining >= 0:
        print(f"Remaining         : {CUR}{remaining:.2f}")
        print("Status: Within budget")
    else:
        print(f"Over budget by    : {CUR}{abs(remaining):.2f}")
        print("Status: Budget exceeded")


# -------------------------------------------------------------------- main ---

def main():
    expenses = load_expenses()
    print(f"Data file: {DATA_FILE}")

    actions = {
        "1": add_expense,
        "2": view_expenses,
        "3": search_expenses,
        "4": update_expense,
        "5": delete_expense,
        "6": show_summary,
        "7": monthly_total,
        "8": show_budget_status,
    }

    try:
        while True:
            print("\n" + "=" * 60)
            print(" STUDENT EXPENSE TRACKER")
            print("=" * 60)
            print("1. Add Expense")
            print("2. View All Expenses")
            print("3. Search Expenses")
            print("4. Update Expense")
            print("5. Delete Expense")
            print("6. Expense Summary")
            print("7. Monthly Total")
            print("8. Budget Status")
            print("9. Exit")

            choice = input("\nEnter your choice: ").strip()

            if choice == "9":
                break
            action = actions.get(choice)
            if action:
                action(expenses)
                # Pause so the result stays visible before the menu redraws.
                input("\nPress ENTER to return to the menu...")
            else:
                print("Invalid choice. Please select 1-9.")
    except (KeyboardInterrupt, EOFError):
        print()

    print("Thank you for using Student Expense Tracker.")


if __name__ == "__main__":
    main()
