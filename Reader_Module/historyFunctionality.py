import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ---------------- Database connection ----------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",   # Change if needed
            database="slms_db"
        )
        return conn
    except Error as e:
        print("Error connecting to database:", e)
        return None


# ---------------- Fetch user borrowing history ----------------
def get_user_history(u_Id):
    """
    Returns a list of dictionaries with the user's past loan records
    Each dictionary contains: title, author, issue_date, return_date, loan_status, fine_amount, due_date
    """
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT lb.u_Id, lb.b_Id, b.title, b.author,
                   lb.issue_date, lb.due_date, lb.return_date,
                   lb.loan_status, lb.fine_amount
            FROM Loan_Record lb
            JOIN Books b ON lb.b_Id = b.b_Id
            WHERE lb.u_Id = %s
            ORDER BY lb.issue_date DESC
        """, (u_Id,))
        records = cursor.fetchall()
        conn.close()

        # Ensure dates are datetime objects
        for r in records:
            if isinstance(r['issue_date'], str):
                r['issue_date'] = datetime.strptime(r['issue_date'], '%Y-%m-%d %H:%M:%S')
            if isinstance(r['due_date'], str):
                r['due_date'] = datetime.strptime(r['due_date'], '%Y-%m-%d')
            if r['return_date'] and isinstance(r['return_date'], str):
                r['return_date'] = datetime.strptime(r['return_date'], '%Y-%m-%d %H:%M:%S')

        return records

    except Error as e:
        print("Error fetching history:", e)
        conn.close()
        return []
