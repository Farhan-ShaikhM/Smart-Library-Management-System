# Admin_Module/adminFunctionality.py
import mysql.connector
from mysql.connector import Error

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
        print("DB connection error:", e)
        return None

def get_admin_stats():
    """
    Returns a dict:
      - overall_books_borrowed : total number of loan records (all time)
      - overall_total_fines    : SUM of fine_amount from Loan_Record
      - overall_active_loans   : count of loans where loan_status = 'Active'
    """
    conn = get_connection()
    if conn is None:
        return {
            "overall_books_borrowed": 0,
            "overall_total_fines": 0.0,
            "overall_active_loans": 0
        }

    cursor = conn.cursor(dictionary=True)
    try:
        # total loans (all time)
        cursor.execute("SELECT COUNT(*) AS total_loans FROM Loan_Record")
        total_loans_row = cursor.fetchone()
        overall_books_borrowed = int(total_loans_row["total_loans"] or 0)

        # total fines collected (profit)
        cursor.execute("SELECT IFNULL(SUM(fine_amount),0) AS total_fines FROM Loan_Record")
        fines_row = cursor.fetchone()
        overall_total_fines = float(fines_row["total_fines"] or 0.0)

        # active loans
        cursor.execute("SELECT COUNT(*) AS active_loans FROM Loan_Record WHERE loan_status = 'Active'")
        active_row = cursor.fetchone()
        overall_active_loans = int(active_row["active_loans"] or 0)

    except Error as e:
        print("Error querying admin stats:", e)
        overall_books_borrowed = 0
        overall_total_fines = 0.0
        overall_active_loans = 0
    finally:
        cursor.close()
        conn.close()

    return {
        "overall_books_borrowed": overall_books_borrowed,
        "overall_total_fines": overall_total_fines,
        "overall_active_loans": overall_active_loans
    }
