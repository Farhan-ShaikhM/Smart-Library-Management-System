# Librarian_Module/requestBooksFunctionality.py
import mysql.connector
from mysql.connector import Error
from datetime import date


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


# ---------- Fetch all vendors ----------
def get_all_vendors():
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT vendor_id, company FROM vendor ORDER BY company ASC;")
        vendors = cursor.fetchall()
        conn.close()
        return vendors
    except Error as e:
        print("Error fetching vendors:", e)
        conn.close()
        return []


# ---------- Fetch librarian requests ----------
def get_librarian_requests(librarian_id):
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT br.request_id, br.book_title, br.author, br.quantity,
                   br.status, br.request_date, v.company AS vendor_name
            FROM book_request br
            JOIN vendor v ON br.vendor_id = v.vendor_id
            WHERE br.librarian_id = %s
            ORDER BY br.request_date DESC;
        """, (librarian_id,))
        data = cursor.fetchall()
        conn.close()
        return data
    except Error as e:
        print("Error fetching requests:", e)
        conn.close()
        return []


# ---------- Send new book request ----------
def send_book_request(librarian_id, vendor_id, title, author, qty):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO book_request (librarian_id, vendor_id, book_title, author, quantity,
                                      request_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Pending');
        """, (librarian_id, vendor_id, title, author, qty, date.today()))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error inserting book request:", e)
        conn.rollback()
        conn.close()
        return False
