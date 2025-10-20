import mysql.connector
from mysql.connector import Error
import re
from tkinter import messagebox

class RegistrationFunctionality:
    def __init__(self, success_callback=None, host="localhost", user="root", password="", database="slms_db"):
        self.success_callback = success_callback
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.conn.is_connected():
                print("Connected to MySQL database for registration")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None

    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        return re.fullmatch(r'\d{10}', phone) is not None

    def register_user(self, full_name, email, password, confirm_password, phone):
        """Register new user and insert into both Users and Reader tables"""
        if not all([full_name, email, password, confirm_password, phone]):
            messagebox.showerror("Error", "All fields are required!")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Phone number must be exactly 10 digits!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if not self.conn:
            messagebox.showerror("Database Error", "Unable to connect to database.")
            return

        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Email already registered!")
                cursor.close()
                return

            # Insert into Users table
            cursor.execute("""
                INSERT INTO Users (name, email, password, role)
                VALUES (%s, %s, %s, %s)
            """, (full_name, email, password, "Reader"))
            self.conn.commit()

            # Fetch u_Id of new user
            cursor.execute("SELECT u_Id FROM Users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                u_Id = user['u_Id']
                cursor.execute("""
                    INSERT INTO Reader (u_Id, phone, date_joined, current_loan_count, overdue_fines)
                    VALUES (%s, %s, CURDATE(), 0, 0.00)
                """, (u_Id, phone))
                self.conn.commit()

                # ✅ Registration successful — trigger success callback
                if self.success_callback:
                    self.success_callback()

            cursor.close()

        except Error as e:
            messagebox.showerror("Database Error", f"MySQL Error: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
