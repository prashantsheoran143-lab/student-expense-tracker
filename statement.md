# Project Statement: Student Expense Tracker

## The problem
Most students spend money in lots of small amounts every day: a snack, an auto fare, a notebook, a recharge. Because each payment is tiny, nobody notices how quickly they add up. By the end of the month it's hard to say where the money went or whether the budget was crossed.

This project is a simple command-line tool where a student can note down each expense and later see where their money is going.

## What I wanted to build
1. A way to record individual expenses
2. Permanent storage in a JSON file, so nothing is lost when the program closes
3. Add, view, update and delete for every record
4. Categories to group expenses
5. Total and average spending
6. Spending per category
7. Spending per month
8. A budget check for a chosen month
9. Something that practises the basics I've learned in Python

## How it's divided
**Managing expenses:** add, view, update and delete.

**Searching:** look up expenses by title, category, date or note.

**Summaries:** total, average, largest expense and category totals.

**Monthly view and budget:** total for a month, and how it compares with a budget the user types in.

## Where the data goes
Everything is saved in `data/expenses.json` on the user's own computer.

## What an expense looks like
Each record has an ID, a title, an amount, a category, a date and an optional note.

## Limits
It's a learning project that runs locally. It doesn't connect to bank accounts, UPI apps or any online service.
