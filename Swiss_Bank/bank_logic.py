import random
from db_config import get_connection

class BankCustomer:
    bank_name = "Swiss Bank Corporation"  # Class Attribute

    def __init__(self, name, email, pin, balance=0.00, acc_no=None):
        self.name = name
        self.email = email
        self.__pin = str(pin)           # Private Attribute
        self.__balance = float(balance)  # Private Attribute
        self.acc_no = acc_no if acc_no else self.generate_account_number()

    @staticmethod
    def generate_account_number():
        return f"SB{random.randint(10000000, 99999999)}"

    @staticmethod
    def validate_pin_format(pin):
        """Validates if the PIN is a 4-digit number."""
        return len(str(pin)) == 4 and str(pin).isdigit()

    @property
    def balance(self):
        """Getter for private balance attribute."""
        return self.__balance

    def verify_pin(self, input_pin):
        """Private attribute access via method."""
        return str(self.__pin) == str(input_pin)

    def deposit(self, amount):
        if amount <= 0:
            return False, "Invalid deposit amount."
        
        conn = get_connection()
        if not conn:
            return False, "Database connection error."
        
        cursor = conn.cursor()
        self.__balance += amount
        
        # Update Balance
        cursor.execute("UPDATE customers SET balance = %s WHERE acc_no = %s", (self.__balance, self.acc_no))
        # Log Transaction
        cursor.execute(
            "INSERT INTO transactions (acc_no, trans_type, amount, balance_after) VALUES (%s, 'Deposit', %s, %s)",
            (self.acc_no, amount, self.__balance)
        )
        conn.commit()
        conn.close()
        return True, f"Successfully deposited ₹{amount:.2f}"

    def withdraw(self, amount):
        if amount <= 0 or amount > self.__balance:
            return False, "Insufficient balance or invalid amount."

        conn = get_connection()
        if not conn:
            return False, "Database connection error."

        cursor = conn.cursor()
        self.__balance -= amount

        # Update Balance
        cursor.execute("UPDATE customers SET balance = %s WHERE acc_no = %s", (self.__balance, self.acc_no))
        # Log Transaction
        cursor.execute(
            "INSERT INTO transactions (acc_no, trans_type, amount, balance_after) VALUES (%s, 'Withdrawal', %s, %s)",
            (self.acc_no, amount, self.__balance)
        )
        conn.commit()
        conn.close()
        return True, f"Successfully withdrew ₹{amount:.2f}"

    def get_passbook(self):
        """Fetches complete transaction history."""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT trans_type, amount, balance_after, timestamp FROM transactions WHERE acc_no = %s ORDER BY timestamp DESC",
            (self.acc_no,)
        )
        records = cursor.fetchall()
        conn.close()
        return records

    def close_account(self):
        """Deactivates account in MySQL database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE customers SET status = 'Closed' WHERE acc_no = %s", (self.acc_no,))
        conn.commit()
        conn.close()
        return "Account closed successfully."