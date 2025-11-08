# Librarian_Module/manageBooksFunctionality.py
import mysql.connector
from mysql.connector import Error

# ---------------- Database Connection ----------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",        # change if needed
            password="",        # change if needed
            database="slms_db"
        )
        return conn
    except Error as e:
        print("Error connecting to database:", e)
        return None


# ---------------- Fetch all books ----------------
def get_all_books():
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b_Id, title, author, main_genre, sub_genre, language,
               available_stock, total_stock, price, aggregate_rating, daily_late_fine
        FROM books ORDER BY title
    """)
    books = cursor.fetchall()
    conn.close()
    return books


# ---------------- Add new book ----------------
def add_new_book(title, author, main_genre, sub_genre, language, total_stock, price, daily_late_fine):
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO books (title, author, main_genre, sub_genre, language,
                               available_stock, total_stock, price, aggregate_rating, daily_late_fine)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0.0, %s)
        """, (title, author, main_genre, sub_genre, language, total_stock, total_stock, price, daily_late_fine))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error adding book:", e)
        conn.rollback()
        conn.close()
        return False


# ---------------- Update existing book ----------------
def update_book(b_Id, title, author, main_genre, sub_genre, language, total_stock, price, daily_late_fine):
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE books
            SET title=%s, author=%s, main_genre=%s, sub_genre=%s, language=%s,
                total_stock=%s, price=%s, daily_late_fine=%s
            WHERE b_Id=%s
        """, (title, author, main_genre, sub_genre, language, total_stock, price, daily_late_fine, b_Id))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error updating book:", e)
        conn.rollback()
        conn.close()
        return False


# ---------------- Delete book ----------------
def delete_book(b_Id):
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM books WHERE b_Id=%s", (b_Id,))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error deleting book:", e)
        conn.rollback()
        conn.close()
        return False
