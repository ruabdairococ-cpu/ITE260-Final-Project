# STUDENT BUDGET MANAGEMENT SYSTEM
# Using Python

transactions = []
balance = 0.0


def add_income():
    global balance

    print("\n--- ADD INCOME ---")
    source = input("Income source: ")
    amount = float(input("Amount: ₱"))

    transactions.append({
        "type": "Income",
        "description": source,
        "amount": amount
    })

    balance += amount
    print(f"Income of ₱{amount:.2f} added successfully!")


def add_expense():
    global balance

    print("\n--- ADD EXPENSE ---")
    description = input("Expense description: ")
    amount = float(input("Amount: ₱"))

    if amount > balance:
        print("Insufficient balance!")
        return

    transactions.append({
        "type": "Expense",
        "description": description,
        "amount": amount
    })

    balance -= amount
    print(f"Expense of ₱{amount:.2f} recorded successfully!")


def view_transactions():
    print("\n--- TRANSACTION HISTORY ---")

    if not transactions:
        print("No transactions recorded yet.")
        return

    print("\nType       Description              Amount")
    print("--------------------------------------------")

    for transaction in transactions:
        print(
            f"{transaction['type']:<10}"
            f"{transaction['description']:<25}"
            f"₱{transaction['amount']:.2f}"
        )


def view_balance():
    print("\n--- CURRENT BALANCE ---")
    print(f"Remaining Budget: ₱{balance:.2f}")


def budget_summary():
    total_income = 0
    total_expenses = 0

    for transaction in transactions:
        if transaction["type"] == "Income":
            total_income += transaction["amount"]
        else:
            total_expenses += transaction["amount"]

    print("\n--- BUDGET SUMMARY ---")
    print(f"Total Income:   ₱{total_income:.2f}")
    print(f"Total Expenses: ₱{total_expenses:.2f}")
    print(f"Remaining:      ₱{total_income - total_expenses:.2f}")


def main():
    while True:
        print("\n===================================")
        print("   STUDENT BUDGET MANAGEMENT SYSTEM")
        print("===================================")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. View Balance")
        print("5. Budget Summary")
        print("6. Exit")
        print("===================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_income()

        elif choice == "2":
            add_expense()

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            view_balance()

        elif choice == "5":
            budget_summary()

        elif choice == "6":
            print("\nThank you for using the Student Budget Management System!")
            break

        else:
            print("Invalid choice. Please try again.")


main()
