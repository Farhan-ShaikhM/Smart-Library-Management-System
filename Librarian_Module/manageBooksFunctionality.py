# Librarian_Module/manageBooksFunctionality.py
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="slms_db"
        )
        return conn
    except Error as e:
        print("DB Connection Error:", e)
        return None


# ----------- Fetch all books -----------
def get_all_books():
    conn = get_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books ORDER BY title ASC;")
        books = cursor.fetchall()
        conn.close()
        return books
    except Error as e:
        print("Error fetching books:", e)
        conn.close()
        return []


# ----------- Add new book -----------
def add_book(title, author, genre, sub_genre, language, stock, price):
    conn = get_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO books (title, author, main_genre, sub_genre, language,
                               available_stock, total_stock, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (title, author, genre, sub_genre, language, stock, stock, price))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error adding book:", e)
        conn.rollback()
        conn.close()
        return False


# ----------- Update book -----------
def update_book(b_Id, title, author, genre, sub_genre, language, stock, price):
    conn = get_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        query = """
            UPDATE books
            SET title=%s, author=%s, main_genre=%s, sub_genre=%s, language=%s,
                available_stock=%s, total_stock=%s, price=%s
            WHERE b_Id=%s;
        """
        cursor.execute(query, (title, author, genre, sub_genre, language, stock, stock, price, b_Id))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error updating book:", e)
        conn.rollback()
        conn.close()
        return False


# ----------- Delete book -----------
def delete_book(b_Id):
    conn = get_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE b_Id=%s;", (b_Id,))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error deleting book:", e)
        conn.rollback()
        conn.close()
        return False
