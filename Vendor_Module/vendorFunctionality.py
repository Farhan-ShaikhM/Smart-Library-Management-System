# Vendor_Module/vendorFunctionality.py
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
        print("Database connection error:", e)
        return None


# ---------- Fetch All Requests for This Vendor ----------
def get_vendor_requests(vendor_id):
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                br.request_id,
                br.book_title,
                br.author,
                br.quantity,
                br.status,
                br.request_date,
                l.u_Id AS librarian_user_id,
                u.name AS librarian_name,
                u.email AS librarian_email
            FROM book_request br
            JOIN librarian l ON br.librarian_id = l.u_Id
            JOIN users u ON l.u_Id = u.u_Id
            WHERE br.vendor_id = %s
            ORDER BY br.request_date DESC;

        """
        cursor.execute(query, (vendor_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Error as e:
        print("Error fetching vendor requests:", e)
        conn.close()
        return []


# ---------- Update Request Status ----------
def update_request_status(request_id, new_status):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE book_request
            SET status = %s
            WHERE request_id = %s;
        """, (new_status, request_id))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error updating request:", e)
        conn.rollback()
        conn.close()
        return False


# ---------- Mark Request as Supplied ----------
def mark_request_supplied(request_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE book_request
            SET status = 'Supplied', supply_date = %s
            WHERE request_id = %s;
        """, (date.today(), request_id))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error marking supplied:", e)
        conn.rollback()
        conn.close()
        return False


# ---------------- Get Vendor by User ID ----------------
def get_vendor_by_user_id(u_Id):
    """Fetch vendor details using the user’s ID (linking vendor → users)."""
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vendor WHERE u_Id = %s", (u_Id,))
        vendor = cursor.fetchone()
        conn.close()
        return vendor
    except Error as e:
        print("Error fetching vendor by user ID:", e)
        conn.close()
        return None

