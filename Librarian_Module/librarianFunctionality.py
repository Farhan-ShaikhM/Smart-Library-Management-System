# Librarian_Module/librarianFunctionality.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ---------------- Database Connection ----------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",       # change if needed
            password="",       # change if needed
            database="slms_db"
        )
        return conn
    except Error as e:
        print("Error connecting to database:", e)
        return None


# ---------------- Fetch dashboard stats ----------------
def get_librarian_dashboard_data():
    """Fetch counts for librarian dashboard"""
    conn = get_connection()
    if conn is None:
        return {}

    cursor = conn.cursor(dictionary=True)
    stats = {}
    try:
        # Total Books
        cursor.execute("SELECT COUNT(*) AS total_books FROM books")
        stats["total_books"] = cursor.fetchone()["total_books"]

        # Total Readers
        cursor.execute("SELECT COUNT(*) AS total_readers FROM reader")
        stats["total_readers"] = cursor.fetchone()["total_readers"]

        # Active Loans
        cursor.execute("SELECT COUNT(*) AS active_loans FROM loan_record WHERE loan_status='Active'")
        stats["active_loans"] = cursor.fetchone()["active_loans"]

        # Overdue Loans
        cursor.execute("""
            SELECT COUNT(*) AS overdue_loans
            FROM loan_record
            WHERE loan_status='Active' AND due_date < %s
        """, (datetime.now().date(),))
        stats["overdue_loans"] = cursor.fetchone()["overdue_loans"]

        conn.close()
        return stats
    except Error as e:
        print("Error fetching librarian stats:", e)
        conn.close()
        return {}
