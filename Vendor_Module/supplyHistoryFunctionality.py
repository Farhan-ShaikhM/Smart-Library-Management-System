# Vendor_Module/supplyHistoryFunctionality.py
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
        print("Database connection error:", e)
        return None


def get_supplied_requests(vendor_id):
    """Fetch all book requests marked as 'Supplied' for a specific vendor."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                br.request_id,
                br.book_title,
                br.author,
                br.quantity,
                br.status,
                br.supply_date,
                u.name AS librarian_name,
                u.email AS librarian_email
            FROM book_request br
            JOIN librarian l ON br.librarian_id = l.u_Id
            JOIN users u ON l.u_Id = u.u_Id
            WHERE br.vendor_id = %s AND br.status = 'Supplied'
            ORDER BY br.supply_date DESC;
        """, (vendor_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Error as e:
        print("Error fetching supply history:", e)
        conn.close()
        return []
