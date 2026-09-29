# 1. Project Title

Student Expense Tracker

# 2. Abstract

Student Expense Tracker is a command-line program written in Python. It lets a user record their expenses, look them up later, and see how much they have spent overall, in each category and in each month. Expenses are saved in a JSON file, so the records are still there after the program is closed and reopened.

Apart from the basic add, view, update and delete operations, the program can search records, work out the total, average and largest expense, and compare a month's spending with a budget the user enters. I kept it to the Python standard library on purpose, because the goal was to practise functions, lists, dictionaries, file handling, input checking and simple testing.

# 3. Problem Statement

Students spend small amounts all through the day, on food, travel, books, recharges and the occasional outing. Since no single payment feels big, it is easy to lose track. At the end of the month there is often no clear answer to how much was spent, what it was spent on, or whether the budget was crossed.

I wanted a simple tool that a student could open, type in an expense in a few seconds, and later get a clear picture from the saved data.

# 4. Objectives

1. Build a small but complete expense manager in Python.
2. Let the user add, view, update and delete expenses.
3. Make it possible to search for an expense.
4. Sort expenses into categories.
5. Show the total, average and largest expense.
6. Show how much was spent in each category and in a given month.
7. Compare a month's spending with a budget.
8. Save the data in a JSON file so it is not lost.
9. Check user input so wrong values do not break the program.
10. Write a few unit tests for the important functions.

# 5. Scope

The program covers adding, viewing, searching, updating and deleting expenses, the eight categories, the summary figures, monthly totals, the budget check, JSON storage, input checking and unit tests.

It does not have a graphical interface, a database server, online banking, cloud sync or any external API. It is meant for one person using it on their own computer.

# 6. Target Users

It is mainly meant for students who want a simple record of their spending. It can also help beginners learning Python who want an example that uses file handling and basic data processing.

# 7. Technologies Used

- Language: Python 3
- Storage: JSON file
- Interface: command line
- Testing: the built-in `unittest` module
- Libraries: only the standard library (`json`, `datetime`, `pathlib`)

Nothing needs to be installed to run it.

# 8. Project Structure

| File or folder | What it is for |
|---|---|
| `expense_tracker.py` | The main program |
| `data/expenses.json` | Saved expenses |
| `tests/test_expense_tracker.py` | Unit tests |
| `README.md` | Short description of the project |
| `statement.md` | Project statement |
| `RUN_PROJECT.txt` | How to run the program |
| `requirements.txt` | Notes on dependencies (there are none) |
| `docs/PROJECT_REPORT.md` | This report |
| `docs/ALGORITHM_AND_FLOW.md` | Step-by-step logic of the main features |

# 9. Expense Categories

The user picks one of eight categories when adding an expense: Food, Travel, Education, Shopping, Entertainment, Bills, Health and Other. Having a fixed list keeps the category totals tidy, since the same category is never typed in two different ways.

# 10. Expense Record

Each expense is stored as a dictionary with six fields:

- `id`: a unique number
- `title`: a short name such as "Lunch" or "Notebook"
- `amount`: the money spent, in rupees
- `category`: one of the eight categories
- `date`: written as YYYY-MM-DD
- `note`: an optional extra remark

The whole collection is a list of these dictionaries, and that list is what gets written to the JSON file.

# 11. Add Expense

The program asks for a title, an amount, a category, a date and an optional note. An empty title is rejected. The amount must be a number greater than zero, and it keeps asking until it gets one. If the user just presses ENTER at the date prompt, today's date is used. The new record gets an ID one higher than the largest ID already in the list, and the list is saved straight away.

# 12. View Expenses

This option prints every saved expense with its ID, date, title, amount and category, with the newest date first. If a note was entered it is shown on the next line. When nothing has been saved yet, the program says so instead of printing an empty screen.

# 13. Search Expenses

The user types a word and the program shows every expense where that word appears in the title, category, date or note. The check ignores capital letters, so "food" and "Food" give the same result. Because the date is also searched, typing something like `2026-09` brings up everything from that month.

# 14. Update Expense

The user enters the ID of the expense to change. The program then goes through each field and shows the current value in brackets. Pressing ENTER leaves that field as it is, so only the things that need fixing have to be retyped. A new amount must still be above zero, and a new date must be in the right format. If the date is wrong, the old date is kept. The changes are saved at the end.

# 15. Delete Expense

After the ID is entered, the program shows the title and amount of that expense and asks for a y or n. The record is removed only if the answer is y. This is there to stop an expense being deleted by a wrong ID or an accidental keypress.

# 16. Total, Average and Largest Expense

The summary option shows:

- the number of expenses
- the **total**, which is all the amounts added together
- the **average**, which is the total divided by the number of expenses
- the **largest expense**, meaning the one with the highest amount

The average is not calculated when there are no expenses, so there is no division by zero. Seeing the largest expense helps a student spot the one purchase that pushed spending up.

# 17. Category-Wise Analysis

The summary screen also groups the amounts by category and prints the totals from highest to lowest. For instance, all the food expenses are added up separately from travel or shopping. This shows quickly which category is taking the biggest share of the money.

# 18. Monthly Analysis

For the monthly total, the user enters a month in the form YYYY-MM. The program adds up every expense whose date starts with that text and prints the result. An invalid month such as `2026-13` is rejected.

# 19. Monthly Budget Status

The user enters a budget and a month. The program works out how much was spent in that month and subtracts it from the budget. If some money is left, it prints the remaining amount and "Within budget". If the spending is higher, it prints how much the budget was exceeded by and "Budget exceeded". The budget has to be greater than zero.

# 20. JSON Data Persistence

Expenses are saved in `data/expenses.json`. JSON was a good fit because it is plain text that can be opened in any editor, and Python can read and write it directly with the `json` module.

The file is read once when the program starts. After every add, update or delete, the whole list is written back to the file. If the file or the `data` folder does not exist yet, it is created automatically. That is why the records survive after the program is closed.

# 21. Input Validation

Anything typed by the user is checked before it is used. The program checks:

- that amounts and budgets are numbers greater than zero
- that the date is a real date in YYYY-MM-DD format
- that the month is in YYYY-MM format
- that the category is a valid number from the list
- that the title and the search text are not empty
- that an expense ID is a whole number that exists

When a value is wrong, the program prints a short message and asks again or returns to the menu. It does not crash.

# 22. Program Flow

```text
START
  |
  v
Load expenses from JSON
  |
  v
Show main menu  <----------------------------+
  |                                          |
  +--> 1 Add Expense ----> validate, save ---+
  +--> 2 View All Expenses ------------------+
  +--> 3 Search Expenses --------------------+
  +--> 4 Update Expense --> validate, save --+
  +--> 5 Delete Expense --> confirm, save ---+
  +--> 6 Expense Summary --------------------+
  +--> 7 Monthly Total ----------------------+
  +--> 8 Budget Status ----------------------+
  |
  +--> 9 Exit
```

# 23. Data Structures

I used only two of Python's built-in structures. A **list** holds all the expenses, and each expense is a **dictionary** with the six fields described earlier. The category totals are also a dictionary, with the category name as the key and the amount as the value. Since JSON maps naturally onto lists and dictionaries, no conversion code was needed.

# 24. File Handling

Saving and loading follow the same simple pattern.

1. Open `expenses.json`.
2. Read the text and convert it into a Python list.
3. Carry out whatever the user asked for.
4. Convert the list back to JSON.
5. Write it to the file.

No database is needed for this, which keeps the project easy to run anywhere.

# 25. Error Handling

There are two places where things can go wrong. The first is user input, which is covered by the validation described above. The second is the data file. If `expenses.json` is empty, damaged, or does not contain a list, the program prints a warning and starts with an empty list instead of stopping with an error message. One thing to be aware of is that the next save will then overwrite the damaged file.

# 26. Testing

The tests are in `tests/test_expense_tracker.py` and use Python's `unittest`. There are five of them, covering:

- generating the next ID
- the total of all expenses
- the category totals
- finding an expense by ID
- the case where an expense ID does not exist

All five pass when run with `python -m unittest discover -s tests -v`. The functions that depend on typed input (adding, updating, deleting) were tested by hand, not by unit tests.

# 27. Advantages

- Simple text menu that is easy to follow
- Data is kept between runs
- Covers add, view, update and delete
- Category, monthly and budget summaries
- Checks user input
- Has unit tests
- Needs no extra packages
- Easy to extend later

# 28. Limitations

- Only a command-line interface, no graphical screen
- JSON is fine for a personal list but not for a very large amount of data
- No login, so anyone with access to the folder can see the data
- No cloud backup
- No link to bank or payment apps
- No charts
- Only one user at a time
- Sorting by date works on the text, so it depends on every date being in YYYY-MM-DD format

# 29. Future Scope

Things I would like to add if I continue working on it:

- A Tkinter or web interface
- Charts for category and monthly spending
- Export to CSV or Excel
- Recurring expenses such as rent or a phone plan
- A separate budget for each category
- A database such as SQLite instead of a JSON file

None of these are part of the current version.

# 30. Conclusion

The Student Expense Tracker does what I set out to do: it lets a student note down expenses quickly and then see the totals by category and by month, and check them against a budget. Writing it gave me practice with functions, lists and dictionaries, reading and writing files, checking input, and writing tests. It is a small project, but it is a working program that could genuinely be used day to day, and it leaves plenty of room to add features later.
