# Algorithm and Flow

## Overall flow
Start -> load expenses from the JSON file -> show the menu -> take the user's choice -> do that task -> save if anything changed -> back to the menu. Choosing 9 exits.

## Adding an expense
1. Ask for a title and stop if it is empty.
2. Ask for the amount. Keep asking until it is a number above zero.
3. Show the category list and let the user pick a number.
4. Ask for the date. Pressing ENTER uses today's date.
5. Ask for an optional note.
6. Give the record the next free ID (highest existing ID + 1).
7. Append it to the list and write the list to the JSON file.

## Updating an expense
1. Ask for the ID and look for it in the list.
2. If it isn't there, say so and go back to the menu.
3. Go through each field. Pressing ENTER keeps the old value.
4. Save the file.

## Deleting an expense
1. Ask for the ID and look for it.
2. Show the title and amount and ask for y/n.
3. Remove it only if the answer is "y", then save.

## Summary
1. Add up all the amounts for the total.
2. Divide the total by the number of expenses for the average.
3. Pick the expense with the highest amount.
4. Add up amounts per category and print them from highest to lowest.

## Budget check
1. Ask for the budget and the month (YYYY-MM).
2. Add up every expense whose date starts with that month.
3. Subtract from the budget.
4. If the result is zero or more, print what is left. Otherwise print how much the budget was exceeded by.
