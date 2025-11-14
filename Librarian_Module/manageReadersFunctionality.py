# Librarian_Module/manageReadersFunctionality.py
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="slms_db"
        )
    except Error as e:
        print("Database Connection Error:", e)
        return None


# ---------- Fetch all readers ----------
def get_all_readers():
    conn = get_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u_Id, name, email, date_of_birth
            FROM users
            WHERE role = 'Reader'
            ORDER BY name ASC;
        """)
        readers = cursor.fetchall()
        conn.close()
        return readers
    except Error as e:
        print("Error fetching readers:", e)
        conn.close()
        return []


# ---------- Update reader ----------
def update_reader(u_Id, name, email, dob):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query = """
            UPDATE users
            SET name=%s, email=%s, date_of_birth=%s
            WHERE u_Id=%s AND role='Reader';
        """
        cursor.execute(query, (name, email, dob, u_Id))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error updating reader:", e)
        conn.rollback()
        conn.close()
        return False


# ---------- Delete reader ----------
def delete_reader(u_Id):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE u_Id=%s AND role='Reader';", (u_Id,))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error deleting reader:", e)
        conn.rollback()
        conn.close()
        return False
