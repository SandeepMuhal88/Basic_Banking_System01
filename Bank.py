import tkinter as tk
from tkinter import messagebox
import random

class Account:
    def __init__(self, name, initial_deposit, pin):
        self.account_number = random.randint(10000, 99999)
        self.name = name
        self.balance = initial_deposit
        self.pin = pin
        self.transactions = [f"Account created with initial deposit of ${initial_deposit}"]

    def verify_pin(self, pin_input):
        return self.pin == pin_input

    def deposit(self, amount, pin_input):
        if not self.verify_pin(pin_input):
            messagebox.showerror("Error", "Invalid PIN!")
            return False
        self.balance += amount
        self.transactions.append(f"Deposited ₹{amount}")
        return True

    def withdraw(self, amount, pin_input):
        if not self.verify_pin(pin_input):
            messagebox.showerror("Error", "Invalid PIN!")
            return False
        if amount > self.balance:
            messagebox.showerror("Error", "Insufficient balance!")
        else:
            self.balance -= amount
            self.transactions.append(f"Withdrew ₹{amount}")
            return True

    def display_balance(self, pin_input):
        if not self.verify_pin(pin_input):
            messagebox.showerror("Error", "Invalid PIN!")
            return None
        return self.balance

    def get_transaction_history(self, pin_input):
        if not self.verify_pin(pin_input):
            messagebox.showerror("Error", "Invalid PIN!")
            return None
        return self.transactions

# GUI Application Class
class BankingApp:
    def __init__(self, root):
        self.accounts = {}  # Store accounts using account number as key
        self.root = root
        self.root.title("Banking System")

        # Main Frame for Account Creation
        self.create_account_frame = tk.Frame(root)
        self.create_account_frame.pack(pady=20)

        tk.Label(self.create_account_frame, text="Create a New Account", font=('Arial', 16)).grid(row=0, columnspan=2, pady=10)

        tk.Label(self.create_account_frame, text="Name:").grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.create_account_frame)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.create_account_frame, text="Initial Deposit:").grid(row=2, column=0, padx=10, pady=5)
        self.deposit_entry = tk.Entry(self.create_account_frame)
        self.deposit_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.create_account_frame, text="PIN:").grid(row=3, column=0, padx=10, pady=5)
        self.pin_entry = tk.Entry(self.create_account_frame, show='*')
        self.pin_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.create_account_frame, text="Create Account", command=self.create_account).grid(row=4, columnspan=2, pady=10)

        # Label to show the last created account number
        self.account_number_label = tk.Label(self.create_account_frame, text="")
        self.account_number_label.grid(row=5, columnspan=2, pady=10)

        # Account Operations Frame
        self.operations_frame = tk.Frame(root)
        self.operations_frame.pack(pady=20)

        tk.Label(self.operations_frame, text="Account Operations", font=('Arial', 16)).grid(row=0, columnspan=2, pady=10)

        tk.Label(self.operations_frame, text="Account Number:").grid(row=1, column=0, padx=10, pady=5)
        self.account_num_entry = tk.Entry(self.operations_frame)
        self.account_num_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.operations_frame, text="PIN:").grid(row=2, column=0, padx=10, pady=5)
        self.operation_pin_entry = tk.Entry(self.operations_frame, show='*')
        self.operation_pin_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.operations_frame, text="Amount:").grid(row=3, column=0, padx=10, pady=5)
        self.amount_entry = tk.Entry(self.operations_frame)
        self.amount_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.operations_frame, text="Deposit", command=self.deposit).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(self.operations_frame, text="Withdraw", command=self.withdraw).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(self.operations_frame, text="Check Balance", command=self.check_balance).grid(row=5, columnspan=2, pady=10)

    def create_account(self):
        name = self.name_entry.get()
        initial_deposit = self.deposit_entry.get()
        pin = self.pin_entry.get()

        if not name or not initial_deposit or not pin:
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            initial_deposit = float(initial_deposit)
        except ValueError:
            messagebox.showerror("Error", "Initial deposit must be a number")
            return

        pin = int(pin)

        # Create the account
        new_account = Account(name, initial_deposit, pin)
        self.accounts[new_account.account_number] = new_account
        
        # Display the account number in a label
        self.account_number_label.config(text=f"Account created successfully! Account Number: {new_account.account_number}")
        
        messagebox.showinfo("Success", f"Account created successfully!\nAccount Number: {new_account.account_number}")
        self.clear_create_account_form()

    def clear_create_account_form(self):
        self.name_entry.delete(0, tk.END)
        self.deposit_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)

    def deposit(self):
        account_num = self.account_num_entry.get()
        amount = self.amount_entry.get()
        pin = self.operation_pin_entry.get()

        if not account_num.isdigit() or int(account_num) not in self.accounts:
            messagebox.showerror("Error", "Account not found")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        account = self.accounts[int(account_num)]
        success = account.deposit(amount, int(pin))

        if success:
            messagebox.showinfo("Success", "Deposit successful")
        self.clear_operation_form()

    def withdraw(self):
        account_num = self.account_num_entry.get()
        amount = self.amount_entry.get()
        pin = self.operation_pin_entry.get()

        if not account_num.isdigit() or int(account_num) not in self.accounts:
            messagebox.showerror("Error", "Account not found")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        account = self.accounts[int(account_num)]
        success = account.withdraw(amount, int(pin))

        if success:
            messagebox.showinfo("Success", "Withdrawal successful")
        self.clear_operation_form()

    def check_balance(self):
        account_num = self.account_num_entry.get()
        pin = self.operation_pin_entry.get()

        if not account_num.isdigit() or int(account_num) not in self.accounts:
            messagebox.showerror("Error", "Account not found")
            return

        account = self.accounts[int(account_num)]
        balance = account.display_balance(int(pin))

        if balance is not None:
            messagebox.showinfo("Balance", f"Current balance: ${balance}")
        self.clear_operation_form()

    def clear_operation_form(self):
        self.account_num_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.operation_pin_entry.delete(0, tk.END)

# Main code to run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()
