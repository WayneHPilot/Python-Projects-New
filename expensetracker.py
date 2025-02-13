# Expense tracker application

# List to store expense records
expenses = []

# Predefined categories
categories = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]

# Function to log an expense
def log_expense():
    try:
        amount = float(input("Enter the expense amount (£): ").strip())
        if amount <= 0:
            print("⚠️ Expense amount must be a positive number.\n")
            return

        print("\nCategories:", ", ".join(categories))
        category = input("Enter the expense category: ").strip().title()
        if category not in categories:
            print("⚠️ Invalid category. Please choose from the listed categories.\n")
            return

        description = input("Enter a brief description of the expense: ").strip()
        if not description:
            print("⚠️ Description cannot be empty.\n")
            return

        expenses.append({"amount": amount, "category": category, "description": description})
        print(f"✅ Expense of £{amount:.2f} added under '{category}' category.\n")

    except ValueError:
        print("⚠️ Invalid amount. Please enter a valid number.\n")

# Function to display expense summary
def view_summary():
    if not expenses:
        print("⚠️ No expenses recorded yet.\n")
        return

    total_spent = sum(exp["amount"] for exp in expenses)
    category_totals = {cat: sum(exp["amount"] for exp in expenses if exp["category"] == cat) for cat in categories}

    print("\n📊 Expense Summary:")
    print(f"💰 Total Amount Spent: £{total_spent:.2f}")
    
    print("\n📌 Spending by Category:")
    for category, total in category_totals.items():
        if total > 0:
            print(f"  - {category}: £{total:.2f}")

    print("\n📜 List of Expenses:")
    for exp in expenses:
        print(f"  - £{exp['amount']:.2f} | {exp['category']} | {exp['description']}")
    print()

# Function to display the menu and handle user choices
def main():
    print("📒 Welcome to the Expense Tracker!\n")

    while True:
        print("📋 Menu:")
        print("1. Log Expense")
        print("2. View Summary")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()
        
        if choice == "1":
            log_expense()
        elif choice == "2":
            view_summary()
        elif choice == "3":
            print("🙏 Thank you for using the Expense Tracker. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Please select a number between 1 and 3.\n")

# Run the program
if __name__ == "__main__":
    main()
