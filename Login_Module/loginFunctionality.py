import mysql.connector
from mysql.connector import Error
import re

class DBAuth:
    def __init__(self, host="localhost", user="root", password="", database="slms_db"):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.conn.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None

    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def login(self, email, password):
        if not email or not password:
            return (False, "Please fill in both fields")

        if not self.validate_email(email):
            return (False, "Invalid email format")

        if not self.conn:
            return (False, "Database connection failed")

        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT * FROM Users WHERE email=%s AND password=%s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            cursor.close()

            if user:
                return (True, user)
            else:
                return (False, "Invalid email or password")
        except Error as e:
            return (False, f"MySQL query error: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
