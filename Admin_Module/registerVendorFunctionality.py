import mysql.connector
from mysql.connector import Error
import re
from tkinter import messagebox
from datetime import date, datetime

class RegisterVendorFunctionality:
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
                print("Connected to MySQL database for librarian registration")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None

    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        return re.fullmatch(r'\d{10}', phone) is not None

    def calculate_age(self, dob: date) -> int:
        today = date.today()
        years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return years

    def register_vendor(self, full_name, email, password, confirm_password, phone, address="", date_of_birth=None):
        """
        Insert into Users (role='Librarian') and Librarian tables.
        Single-cursor implementation.
        """
        if not all([full_name, email, password, confirm_password, phone]):
            messagebox.showerror("Error", "Full name, email, phone and password fields are required!")
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

        # validate dob if provided
        dob_obj = None
        if date_of_birth:
            if isinstance(date_of_birth, date):
                dob_obj = date_of_birth
            else:
                try:
                    dob_obj = datetime.strptime(str(date_of_birth), "%Y-%m-%d").date()
                except Exception:
                    messagebox.showerror("Error", "Date of birth must be a valid date (YYYY-MM-DD).")
                    return

            age = self.calculate_age(dob_obj)
            if age < 18 or age > 80:
                messagebox.showerror("Error", "Vendor must be at least 18 years old and under 80 years old.")
                return

        if not self.conn:
            messagebox.showerror("Database Error", "Unable to connect to database.")
            return

        try:
            cursor = self.conn.cursor(dictionary=True)

            # check existing email
            cursor.execute("SELECT u_Id FROM Users WHERE email = %s", (email,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Email already registered!")
                cursor.close()
                return

            # Insert into Users (role = 'Librarian')
            cursor.execute("""
                INSERT INTO Users (name, email, password, role, date_of_birth)
                VALUES (%s, %s, %s, %s, %s)
            """, (full_name, email, password, "Vendor", dob_obj))
            self.conn.commit()

            # lastrowid works on this cursor
            u_Id = cursor.lastrowid
            if not u_Id:
                # fallback: query by email
                cursor.execute("SELECT u_Id FROM Users WHERE email = %s", (email,))
                r = cursor.fetchone()
                u_Id = r['u_Id'] if r else None

                # trigger success callback (UI will handle closing and returning to admin)
                if self.success_callback:
                    try:
                        self.success_callback()
                    except Exception:
                        pass

            cursor.close()

        except Error as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            messagebox.showerror("Database Error", f"MySQL Error: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
