# Admin_Module/manageBooksFunctionality.py
import mysql.connector
from mysql.connector import Error
from decimal import Decimal

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",    # change if needed
    "database": "slms_db"
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("DB connection error:", e)
        return None

def get_all_books():
    """
    Returns a list of dicts with all book columns.
    """
    conn = get_connection()
    if not conn:
        return []

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT b_Id, title, author, main_genre, sub_genre, language,
                   available_stock, total_stock, price, aggregate_rating, daily_late_fine
            FROM Books
            ORDER BY title
        """)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print("Error fetching books:", e)
        return []
    finally:
        cursor.close()
        conn.close()

def get_book_by_id(b_Id):
    conn = get_connection()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT b_Id, title, author, main_genre, sub_genre, language,
                   available_stock, total_stock, price, aggregate_rating, daily_late_fine
            FROM Books
            WHERE b_Id = %s
            LIMIT 1
        """, (b_Id,))
        row = cursor.fetchone()
        return row
    except Error as e:
        print("Error fetching book:", e)
        return None
    finally:
        cursor.close()
        conn.close()

def insert_book(data: dict):
    """
    Insert a new book. Expected keys: title, author, main_genre, sub_genre, language,
    available_stock, total_stock, price, aggregate_rating, daily_late_fine
    Returns (True, new_b_Id) on success or (False, error_message)
    """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed"

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Books
            (title, author, main_genre, sub_genre, language, available_stock, total_stock, price, aggregate_rating, daily_late_fine)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data.get("title"),
            data.get("author"),
            data.get("main_genre"),
            data.get("sub_genre"),
            data.get("language"),
            int(data.get("available_stock")),
            int(data.get("total_stock")),
            Decimal(str(data.get("price"))),
            Decimal(str(data.get("aggregate_rating"))),
            Decimal(str(data.get("daily_late_fine")))
        ))
        conn.commit()
        new_id = cursor.lastrowid
        return True, new_id
    except Error as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def update_book(b_Id, data: dict):
    """
    Update an existing book.
    Returns (True, None) on success or (False, error_message)
    """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed"

    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Books SET
                title=%s,
                author=%s,
                main_genre=%s,
                sub_genre=%s,
                language=%s,
                available_stock=%s,
                total_stock=%s,
                price=%s,
                aggregate_rating=%s,
                daily_late_fine=%s
            WHERE b_Id=%s
        """, (
            data.get("title"),
            data.get("author"),
            data.get("main_genre"),
            data.get("sub_genre"),
            data.get("language"),
            int(data.get("available_stock")),
            int(data.get("total_stock")),
            Decimal(str(data.get("price"))),
            Decimal(str(data.get("aggregate_rating"))),
            Decimal(str(data.get("daily_late_fine"))),
            b_Id
        ))
        conn.commit()
        return True, None
    except Error as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def delete_book(b_Id):
    """
    Attempt to delete a book. If FK constraints prevent deletion, this will fail.
    Returns (True, None) on success or (False, error_message)
    """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Books WHERE b_Id = %s", (b_Id,))
        if cursor.rowcount == 0:
            conn.close()
            return False, "Book not found"
        conn.commit()
        return True, None
    except Error as e:
        try:
            conn.rollback()
        except Exception:
            pass
        # If there are loan records or other FK references, MySQL will throw an error
        return False, str(e)
    finally:
        cursor.close()
        conn.close()
