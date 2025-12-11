# Librarian_Module/loanRecordsFunctionality.py
import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta


def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="slms_db"
        )
    except Error as e:
        print("DB Connection Error:", e)
        return None


# ---------- Fetch All Loan Records ----------
def get_all_loans(filter_status="All"):
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT
                lr.loan_id,
                u.name AS reader_name,
                b.title,
                b.author,
                lr.issue_date,
                lr.due_date,
                lr.return_date,
                lr.loan_status
            FROM loan_record lr
            JOIN users u ON lr.u_Id = u.u_Id
            JOIN books b ON lr.b_Id = b.b_Id
        """

        # Filter logic
        if filter_status == "Active":
            query += " WHERE lr.loan_status = 'Active'"
        elif filter_status == "Returned":
            query += " WHERE lr.loan_status LIKE 'Returned%'"
        elif filter_status == "Overdue":
            query += " WHERE lr.loan_status = 'Active' AND lr.due_date < CURDATE()"
        elif filter_status == "Lost":
            query += " WHERE lr.loan_status = 'Lost'"

        query += " ORDER BY lr.issue_date DESC;"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Error as e:
        print("Error fetching loan records:", e)
        conn.close()
        return []


# ---------- Issue a Book ----------
def issue_book(u_Id, b_Id, days=15):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        issue_date = date.today()
        due_date = issue_date + timedelta(days=days)

        # Decrease available stock
        cursor.execute(
            "UPDATE books SET available_stock = available_stock - 1 WHERE b_Id=%s AND available_stock > 0;",
            (b_Id,)
        )
        if cursor.rowcount == 0:
            raise Exception("No available stock!")

        # Insert loan record
        cursor.execute("""
            INSERT INTO loan_record (u_Id, b_Id, issue_date, due_date, loan_status)
            VALUES (%s, %s, %s, %s, 'Active');
        """, (u_Id, b_Id, issue_date, due_date))

        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error issuing book:", e)
        conn.rollback()
        conn.close()
        return False


# ---------- Mark as Returned ----------
def mark_as_returned(loan_id):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        # Fetch due_date
        cursor.execute("SELECT b_Id, due_date FROM loan_record WHERE loan_id=%s", (loan_id,))
        record = cursor.fetchone()
        if not record:
            raise Exception("Loan not found!")

        b_Id, due_date = record
        today = date.today()
        status = "Returned - On Time" if today <= due_date else "Returned - Late"

        cursor.execute("""
            UPDATE loan_record
            SET return_date=%s, loan_status=%s
            WHERE loan_id=%s;
        """, (today, status, loan_id))

        # Increase stock
        cursor.execute("UPDATE books SET available_stock = available_stock + 1 WHERE b_Id=%s;", (b_Id,))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error marking return:", e)
        conn.rollback()
        conn.close()
        return False
