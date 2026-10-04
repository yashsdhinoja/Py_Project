import tkinter as tk
from tkinter import messagebox, ttk
from bank_logic import BankCustomer
from db_config import get_connection

class SwissBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Swiss Bank - Core Banking Application")
        self.root.geometry("500x500")
        self.current_user = None

        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()
        
        tk.Label(self.main_frame, text="Swiss Bank", font=("Helvetica", 18, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Account Number:").pack(anchor="w")
        acc_entry = tk.Entry(self.main_frame)
        acc_entry.pack(fill="x", pady=5)

        tk.Label(self.main_frame, text="4-Digit PIN:").pack(anchor="w")
        pin_entry = tk.Entry(self.main_frame, show="*")
        pin_entry.pack(fill="x", pady=5)

        def login():
            acc_no = acc_entry.get().strip()
            pin = pin_entry.get().strip()

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM customers WHERE acc_no = %s AND status = 'Active'", (acc_no,))
            data = cursor.fetchone()
            conn.close()

            if data and data['pin'] == pin:
                self.current_user = BankCustomer(
                    name=data['name'], 
                    email=data['email'], 
                    pin=data['pin'], 
                    balance=data['balance'], 
                    acc_no=data['acc_no']
                )
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid Account Number or PIN.")

        tk.Button(self.main_frame, text="Login", command=login, bg="#2b5c8f", fg="white").pack(fill="x", pady=10)
        tk.Button(self.main_frame, text="Open New Account", command=self.show_register_screen).pack(fill="x")

    def show_register_screen(self):
        self.clear_screen()
        tk.Label(self.main_frame, text="Open Swiss Bank Account", font=("Helvetica", 14, "bold")).pack(pady=10)

        tk.Label(self.main_frame, text="Full Name:").pack(anchor="w")
        name_entry = tk.Entry(self.main_frame)
        name_entry.pack(fill="x", pady=2)

        tk.Label(self.main_frame, text="Email:").pack(anchor="w")
        email_entry = tk.Entry(self.main_frame)
        email_entry.pack(fill="x", pady=2)

        tk.Label(self.main_frame, text="Set 4-Digit PIN:").pack(anchor="w")
        pin_entry = tk.Entry(self.main_frame, show="*")
        pin_entry.pack(fill="x", pady=2)

        def register():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            pin = pin_entry.get().strip()

            if not BankCustomer.validate_pin_format(pin):
                messagebox.showerror("Error", "PIN must be exactly 4 digits.")
                return

            customer = BankCustomer(name, email, pin)
            conn = get_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute(
                    "INSERT INTO customers (acc_no, name, email, pin, balance) VALUES (%s, %s, %s, %s, %s)",
                    (customer.acc_no, customer.name, customer.email, pin, customer.balance)
                )
                conn.commit()
                messagebox.showinfo("Success", f"Account Opened Successfully!\nYour Account No: {customer.acc_no}")
                self.show_login_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open account: {e}")
            finally:
                conn.close()

        tk.Button(self.main_frame, text="Submit", command=register, bg="green", fg="white").pack(fill="x", pady=10)
        tk.Button(self.main_frame, text="Back to Login", command=self.show_login_screen).pack(fill="x")

    def show_dashboard(self):
        self.clear_screen()
        tk.Label(self.main_frame, text=f"Welcome, {self.current_user.name}", font=("Helvetica", 14, "bold")).pack(pady=5)
        
        self.balance_lbl = tk.Label(self.main_frame, text=f"Balance: ₹{self.current_user.balance:.2f}", font=("Helvetica", 12))
        self.balance_lbl.pack(pady=5)

        tk.Button(self.main_frame, text="Deposit Money", command=self.deposit_ui).pack(fill="x", pady=3)
        tk.Button(self.main_frame, text="Withdraw Money", command=self.withdraw_ui).pack(fill="x", pady=3)
        tk.Button(self.main_frame, text="Passbook (Transactions)", command=self.passbook_ui).pack(fill="x", pady=3)
        tk.Button(self.main_frame, text="Close Account", command=self.close_acc_ui, bg="red", fg="white").pack(fill="x", pady=3)
        tk.Button(self.main_frame, text="Logout", command=self.show_login_screen).pack(fill="x", pady=10)

    def deposit_ui(self):
        amount = tk.simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount:
            success, msg = self.current_user.deposit(amount)
            messagebox.showinfo("Result", msg)
            self.balance_lbl.config(text=f"Balance: ₹{self.current_user.balance:.2f}")

    def withdraw_ui(self):
        amount = tk.simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount:
            success, msg = self.current_user.withdraw(amount)
            messagebox.showinfo("Result", msg)
            self.balance_lbl.config(text=f"Balance: ₹{self.current_user.balance:.2f}")

    def passbook_ui(self):
        passbook_win = tk.Toplevel(self.root)
        passbook_win.title("Passbook - Transaction History")
        passbook_win.geometry("450x300")

        cols = ("Type", "Amount", "Balance After", "Timestamp")
        tree = ttk.Treeview(passbook_win, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        records = self.current_user.get_passbook()
        for rec in records:
            tree.insert("", tk.END, values=(rec['trans_type'], f"₹{rec['amount']}", f"₹{rec['balance_after']}", rec['timestamp']))

    def close_acc_ui(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to close your account?")
        if confirm:
            msg = self.current_user.close_account()
            messagebox.showinfo("Account Status", msg)
            self.show_login_screen()