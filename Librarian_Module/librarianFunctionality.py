# Librarian_Module/librarianFunctionality.py
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="slms_db",
        )
        return conn
    except Error as e:
        print("DB connection error:", e)
        return None


def get_librarian_summary(u_Id=None):
    data = {"total_books": 0, "total_readers": 0, "active_loans": 0}
    conn = get_connection()
    if not conn:
        return data

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM books;")
        data["total_books"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM users WHERE role='Reader';")
        data["total_readers"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM loan_record WHERE loan_status='Active';")
        data["active_loans"] = cursor.fetchone()[0]

        conn.close()
        return data
    except Error as e:
        print("Error fetching librarian summary:", e)
        conn.close()
        return data
