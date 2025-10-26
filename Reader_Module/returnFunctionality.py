import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ---------------- Database connection ----------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",       # change if needed
            database="slms_db"
        )
        return conn
    except Error as e:
        print("Error connecting to database:", e)
        return None

# ---------------- Fetch borrowed books for user ----------------
def get_user_borrowed_books_with_dates(u_Id):
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT lb.b_Id, b.title, b.author, lb.issue_date, lb.due_date, b.daily_late_fine, b.price
        FROM Loan_Record lb
        JOIN Books b ON lb.b_Id = b.b_Id
        WHERE lb.u_Id = %s AND lb.loan_status = 'Active'
    """, (u_Id,))
    books = cursor.fetchall()
    conn.close()
    return books

# ---------------- Return a book ----------------
def return_book(u_Id, b_Id, rating, status, return_date=None):
    conn = get_connection()
    if conn is None:
        return False, "Database connection failed"

    cursor = conn.cursor()

    try:
        if return_date is None:
            return_date = datetime.now()

        # Fetch issue_date, due_date, daily_late_fine, and price
        cursor.execute("""
            SELECT lb.issue_date, lb.due_date, b.daily_late_fine, b.price
            FROM Loan_Record lb
            JOIN Books b ON lb.b_Id = b.b_Id
            WHERE lb.u_Id=%s AND lb.b_Id=%s AND lb.loan_status='Active'
        """, (u_Id, b_Id))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, "Loan record not found"

        issue_date, due_date, daily_late_fine, price = row
        daily_late_fine = float(daily_late_fine or 0.50)
        price = float(price or 0.0)

        # Calculate fine
        if status == "Lost":
            fine = price  # full price of the book
            new_status = "Lost"
        else:
            days_overdue = max((return_date.date() - due_date).days, 0)
            fine = days_overdue * daily_late_fine
            new_status = "Returned - On Time" if days_overdue == 0 else "Returned - Late"

        # Update Loan_Record
        cursor.execute("""
            UPDATE Loan_Record
            SET loan_status=%s, return_date=%s, fine_amount=%s
            WHERE u_Id=%s AND b_Id=%s AND loan_status='Active'
        """, (new_status, return_date, fine, u_Id, b_Id))

        # Update Books stock if returned
        if status == "Returned":
            cursor.execute("UPDATE Books SET available_stock = available_stock + 1 WHERE b_Id=%s", (b_Id,))

        # Insert/update Personal_Rating
        cursor.execute("""
            INSERT INTO Personal_Rating(u_Id, b_Id, rating_value)
            VALUES(%s, %s, %s)
            ON DUPLICATE KEY UPDATE rating_value=%s, rating_date=CURRENT_TIMESTAMP
        """, (u_Id, b_Id, rating, rating))

        # Update Reader's overdue fines and current loan count
        cursor.execute("""
            UPDATE Reader
            SET current_loan_count = current_loan_count - 1,
                overdue_fines = overdue_fines + %s
            WHERE u_Id=%s
        """, (fine, u_Id))

        conn.commit()
        conn.close()
        return True, fine

    except Error as e:
        conn.rollback()
        conn.close()
        return False, str(e)
