
import json
from datetime import date
from pathlib import Path


FILE_NAME = "expenses.json"


def load_expenses():
    if not Path(FILE_NAME).exists():
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Warning: expense file is invalid. Starting with an empty list.")
        return []


def save_expenses(expenses):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4, ensure_ascii=False)


def add_expense(expenses):
    description = input("Description: ").strip()
    category = input("Category: ").strip()

    if not description or not category:
        print("Description and category cannot be empty.")
        return

    try:
        amount_text = input("Amount in RON: ").strip().replace(",", ".")
        amount = float(amount_text)

        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid amount, for example 25.50.")
        return

    expense = {
        "description": description,
        "category": category,
        "amount": round(amount, 2),
        "date": date.today().isoformat()
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully!")


def show_expenses(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n=== EXPENSE HISTORY ===")

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. {expense['date']} | "
            f"{expense['description']} | "
            f"{expense['category']} | "
            f"{expense['amount']:.2f} RON"
        )


def show_total(expenses):
    total = sum(expense["amount"] for expense in expenses)
    print(f"\nTotal expenses: {total:.2f} RON")


def show_category_totals(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    totals = {}

    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]

    print("\n=== TOTALS BY CATEGORY ===")

    for category, total in sorted(totals.items()):
        print(f"{category}: {total:.2f} RON")


def main():
    expenses = load_expenses()

    while True:
        print("\n=== PYTHON EXPENSE TRACKER ===")
        print("1. Add expense")
        print("2. Show expense history")
        print("3. Show total expenses")
        print("4. Show totals by category")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            show_total(expenses)
        elif choice == "4":
            show_category_totals(expenses)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
