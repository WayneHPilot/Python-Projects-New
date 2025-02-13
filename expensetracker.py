import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      amount REAL,
                      category TEXT,
                      description TEXT)''')
    conn.commit()
    conn.close()

# Function to add an expense
def add_expense():
    try:
        amount = float(amount_entry.get())
        category = category_var.get()
        description = desc_entry.get()
        
        if amount <= 0 or not description.strip():
            messagebox.showerror("Input Error", "Amount must be positive and description cannot be empty!")
            return
        
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)",
                       (amount, category, description))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Expense added successfully!")
        amount_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        view_expenses()  # Refresh the table
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid amount!")

# Function to view expenses and update GUI
def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT amount, category, description FROM expenses")
    expenses = cursor.fetchall()
    conn.close()

    # Clear the existing rows in the Treeview
    for row in expense_tree.get_children():
        expense_tree.delete(row)

    # Insert new rows into the Treeview
    for expense in expenses:
        expense_tree.insert("", "end", values=expense)

# GUI Setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x500")

# Widgets
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Amount (£):").grid(row=0, column=0, padx=5, pady=5)
amount_entry = tk.Entry(frame, width=25)  # Adjust width for uniformity
amount_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
category_var = tk.StringVar()
categories = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]
category_menu = ttk.Combobox(frame, textvariable=category_var, values=categories, state="readonly", width=22)  # Match width
category_menu.grid(row=1, column=1, padx=5, pady=5)
category_menu.current(0)

tk.Label(frame, text="Description:").grid(row=2, column=0, padx=5, pady=5)
desc_entry = tk.Entry(frame, width=25)  # Match width
desc_entry.grid(row=2, column=1, padx=5, pady=5)


tk.Button(frame, text="Add Expense", command=add_expense).grid(row=3, columnspan=2, pady=10)

# Expense List (Table)
expense_tree = ttk.Treeview(root, columns=("Amount", "Category", "Description"), show="headings", height=10)
expense_tree.heading("Amount", text="Amount (£)")
expense_tree.heading("Category", text="Category")
expense_tree.heading("Description", text="Description")
expense_tree.column("Amount", width=100, anchor="center")
expense_tree.column("Category", width=150, anchor="center")
expense_tree.column("Description", width=200, anchor="center")
expense_tree.pack(pady=10)

# Initialize DB, load existing expenses, and run the app
init_db()
view_expenses()
root.mainloop()
