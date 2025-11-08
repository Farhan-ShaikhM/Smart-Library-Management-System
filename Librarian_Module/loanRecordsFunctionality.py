# Librarian_Module/loanRecordsFunctionality.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime, date

# ---------------- Database Connection ----------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # change if needed
            password="",  # change if needed
            database="slms_db"
        )
        return conn
    except Error as e:
        print("Error connecting to DB:", e)
        return None


# ---------------- Fetch all loan records ----------------
def get_all_loans(status_filter=None):
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT lr.loan_id, lr.u_Id, lr.b_Id, lr.issue_date, lr.due_date, lr.return_date, 
               lr.loan_status, lr.fine_amount, b.title, b.author, b.daily_late_fine,
               u.name AS reader_name
        FROM loan_record lr
        JOIN books b ON lr.b_Id = b.b_Id
        JOIN users u ON lr.u_Id = u.u_Id
    """
    if status_filter and status_filter != "All" and status_filter != "Overdue":
        query += " WHERE lr.loan_status = %s"
        cursor.execute(query, (status_filter,))
    else:
        cursor.execute(query)

    loans = cursor.fetchall()
    conn.close()
    return loans


# ---------------- Fetch overdue loans ----------------
def get_overdue_loans():
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT lr.loan_id, lr.u_Id, lr.b_Id, lr.issue_date, lr.due_date, lr.loan_status,
               b.title, u.name AS reader_name, b.daily_late_fine
        FROM loan_record lr
        JOIN books b ON lr.b_Id = b.b_Id
        JOIN users u ON lr.u_Id = u.u_Id
        WHERE lr.loan_status='Active' AND lr.due_date < CURDATE()
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------------- Update loan status (with optional fine) ----------------
def update_loan_status(loan_id, new_status, fine=0.0):
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        return_date = datetime.now()

        cursor.execute("""
            UPDATE loan_record
            SET loan_status=%s, return_date=%s, fine_amount=%s
            WHERE loan_id=%s
        """, (new_status, return_date, fine, loan_id))

        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error updating loan status:", e)
        conn.rollback()
        conn.close()
        return False


# ---------------- Increment available stock on book return ----------------
def increment_book_stock(b_Id):
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE books SET available_stock = available_stock + 1 WHERE b_Id = %s", (b_Id,))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error incrementing book stock:", e)
        conn.rollback()
        conn.close()
        return False
