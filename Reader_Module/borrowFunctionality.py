import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

# ---------------- Database connection ----------------
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

# ---------------- Fetch available books ----------------
def get_available_books():
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b_Id, title, author, main_genre, aggregate_rating, available_stock
        FROM Books
        WHERE available_stock > 0
        ORDER BY title
    """)
    books = cursor.fetchall()
    conn.close()
    return books

# ---------------- Borrow a book for a user ----------------
def borrow_book_for_user(u_Id, b_Id):
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # Check available stock
        cursor.execute("SELECT available_stock FROM Books WHERE b_Id=%s", (b_Id,))
        stock = cursor.fetchone()
        if not stock or stock[0] <= 0:
            conn.close()
            return False

        # Insert loan record
        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=10)
        cursor.execute("""
            INSERT INTO Loan_Record (u_Id, b_Id, issue_date, due_date, loan_status)
            VALUES (%s, %s, %s, %s, 'Active')
        """, (u_Id, b_Id, issue_date, due_date))

        # Update stock and user's loan count
        cursor.execute("UPDATE Books SET available_stock = available_stock - 1 WHERE b_Id=%s", (b_Id,))
        cursor.execute("UPDATE Reader SET current_loan_count = current_loan_count + 1 WHERE u_Id=%s", (u_Id,))

        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error borrowing book:", e)
        conn.rollback()
        conn.close()
        return False

# ---------------- Get user's borrowed books ----------------
def get_user_borrowed_books(u_Id):
    try:
        conn = get_connection()
        if conn is None:
            return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT b_Id FROM Loan_Record WHERE u_Id = %s AND loan_status = 'Active'", (u_Id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return [row["b_Id"] for row in results]
    except Exception as e:
        print("Error fetching borrowed books:", e)
        return []
