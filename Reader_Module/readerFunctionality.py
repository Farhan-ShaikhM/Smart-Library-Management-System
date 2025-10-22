import mysql.connector
from mysql.connector import Error

# ---------------- Database connection ----------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          # change if needed
            password="",          # change if needed
            database="slms_db"
        )
        return conn
    except Error as e:
        print("Error connecting to database:", e)
        return None


# ---------------- Reader Data ----------------
def get_reader_data(u_Id):
    """
    Fetch reader details and stats from database.
    Returns a dictionary with:
    full_name, u_Id, remark, total_books_read, total_fines, active_loans
    """
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)

    # Get reader full name and remark
    cursor.execute("""
        SELECT u.name, r.user_remark
        FROM Users u
        JOIN Reader r ON u.u_Id = r.u_Id
        WHERE u.u_Id = %s
    """, (u_Id,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return None

    # Total books read (returned)
    cursor.execute("""
        SELECT COUNT(*) as total_books_read
        FROM Loan_Record
        WHERE u_Id=%s AND loan_status LIKE 'Returned%'
    """, (u_Id,))
    total_books_read = cursor.fetchone()
    total_books_read = total_books_read["total_books_read"] if total_books_read else 0

    # Total fines
    cursor.execute("""
        SELECT IFNULL(SUM(fine_amount), 0) as total_fines
        FROM Loan_Record
        WHERE u_Id=%s
    """, (u_Id,))
    total_fines = cursor.fetchone()
    total_fines = total_fines["total_fines"] if total_fines else 0

    # Active loans
    cursor.execute("""
        SELECT COUNT(*) as active_loans
        FROM Loan_Record
        WHERE u_Id=%s AND loan_status='Active'
    """, (u_Id,))
    active_loans = cursor.fetchone()
    active_loans = active_loans["active_loans"] if active_loans else 0

    conn.close()

    return {
        "full_name": user["name"],
        "u_Id": u_Id,
        "remark": user.get("user_remark", "No remarks"),
        "total_books_read": total_books_read or 0,
        "total_fines": total_fines or 0,
        "active_loans": active_loans or 0
    }


# ---------------- Placeholder Functionalities ----------------
def borrow_book(u_Id, b_Id):
    # Logic to borrow a book will go here
    print(f"Borrow book {b_Id} for user {u_Id}")
    return True


def return_book(u_Id, loan_id):
    # Logic to return a book will go here
    print(f"Return loan {loan_id} for user {u_Id}")
    return True


def get_recommendations(u_Id):
    # Logic to get recommendations will go here
    print(f"Get recommendations for user {u_Id}")
    return ["Book 1", "Book 2", "Book 3"]
