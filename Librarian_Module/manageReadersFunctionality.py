# Librarian_Module/manageReadersFunctionality.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ---------------- DB connection ----------------
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

# ---------------- Fetch all readers with basic info ----------------
def get_all_readers():
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT r.u_Id, u.name, u.email, r.phone, r.date_joined, r.current_loan_count, r.overdue_fines, r.user_remark
            FROM reader r
            JOIN users u ON r.u_Id = u.u_Id
            ORDER BY u.name
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Error as e:
        print("Error fetching readers:", e)
        conn.close()
        return []

# ---------------- Fetch detailed reader info ----------------
def get_reader_details(u_Id):
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)
    try:
        # basic info
        cursor.execute("""
            SELECT r.u_Id, u.name, u.email, r.phone, r.date_joined, r.current_loan_count, r.overdue_fines, r.user_remark
            FROM reader r
            JOIN users u ON r.u_Id = u.u_Id
            WHERE r.u_Id = %s
        """, (u_Id,))
        reader = cursor.fetchone()

        if not reader:
            conn.close()
            return None

        # active loans
        cursor.execute("""
            SELECT lr.loan_id, lr.b_Id, b.title, b.author, lr.issue_date, lr.due_date, lr.loan_status
            FROM loan_record lr
            JOIN books b ON lr.b_Id = b.b_Id
            WHERE lr.u_Id = %s AND lr.loan_status = 'Active'
            ORDER BY lr.issue_date DESC
        """, (u_Id,))
        active_loans = cursor.fetchall()

        # past loans (recent 10)
        cursor.execute("""
            SELECT lr.loan_id, lr.b_Id, b.title, b.author, lr.issue_date, lr.due_date, lr.return_date, lr.loan_status, lr.fine_amount
            FROM loan_record lr
            JOIN books b ON lr.b_Id = b.b_Id
            WHERE lr.u_Id = %s
            ORDER BY lr.issue_date DESC
            LIMIT 10
        """, (u_Id,))
        recent_loans = cursor.fetchall()

        conn.close()
        reader['active_loans'] = active_loans
        reader['recent_loans'] = recent_loans
        return reader

    except Error as e:
        print("Error fetching reader details:", e)
        conn.close()
        return None

# ---------------- Update reader remark ----------------
def update_reader_remark(u_Id, remark):
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE reader SET user_remark = %s WHERE u_Id = %s", (remark, u_Id))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error updating remark:", e)
        conn.rollback()
        conn.close()
        return False

# ---------------- Clear overdue fines (set to 0 and adjust field) ----------------
def clear_overdue_fines(u_Id):
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE reader SET overdue_fines = 0.00 WHERE u_Id = %s", (u_Id,))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error clearing fines:", e)
        conn.rollback()
        conn.close()
        return False

# ---------------- Adjust current loan count (helper) ----------------
def set_current_loan_count(u_Id, new_count):
    conn = get_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE reader SET current_loan_count = %s WHERE u_Id = %s", (new_count, u_Id))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error setting loan count:", e)
        conn.rollback()
        conn.close()
        return False
