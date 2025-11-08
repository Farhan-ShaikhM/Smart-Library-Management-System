# Vendor_Module/vendorFunctionality.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ---------------- Database Connection ----------------
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


# ======================================================
#                  VENDOR MANAGEMENT
# ======================================================

def get_all_vendors():
    """Return list of all vendors"""
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vendor ORDER BY vendor_name")
    vendors = cursor.fetchall()
    conn.close()
    return vendors


def add_vendor(vendor_name, contact_person, email, phone, address):
    """Add new vendor"""
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO vendor (vendor_name, contact_person, email, phone, address)
            VALUES (%s, %s, %s, %s, %s)
        """, (vendor_name, contact_person, email, phone, address))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error adding vendor:", e)
        conn.rollback()
        conn.close()
        return False


def update_vendor(vendor_id, vendor_name, contact_person, email, phone, address):
    """Update vendor info"""
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE vendor
            SET vendor_name=%s, contact_person=%s, email=%s, phone=%s, address=%s
            WHERE vendor_id=%s
        """, (vendor_name, contact_person, email, phone, address, vendor_id))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error updating vendor:", e)
        conn.rollback()
        conn.close()
        return False


def delete_vendor(vendor_id):
    """Delete a vendor"""
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM vendor WHERE vendor_id=%s", (vendor_id,))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error deleting vendor:", e)
        conn.rollback()
        conn.close()
        return False


# ======================================================
#                  SUPPLY BATCH MANAGEMENT
# ======================================================

def create_supply_batch(vendor_id, items):
    """
    Create a new supply batch and add supplied book items.
    items should be a list of dicts like:
    [
        {"b_Id": 1, "quantity": 10, "cost_price": 250.0},
        {"b_Id": 2, "quantity": 5, "cost_price": 300.0}
    ]
    """
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # 1️⃣ Insert supply batch header
        cursor.execute("""
            INSERT INTO supply_batch (vendor_id, delivery_date, status, total_cost)
            VALUES (%s, %s, 'Pending', 0)
        """, (vendor_id, datetime.now().date()))
        batch_id = cursor.lastrowid

        total_cost = 0
        # 2️⃣ Insert each supplied book item
        for item in items:
            cursor.execute("""
                INSERT INTO supply_batch_items (batch_id, b_Id, quantity, cost_price)
                VALUES (%s, %s, %s, %s)
            """, (batch_id, item["b_Id"], item["quantity"], item["cost_price"]))
            total_cost += item["quantity"] * item["cost_price"]

        # 3️⃣ Update total cost
        cursor.execute("UPDATE supply_batch SET total_cost=%s WHERE batch_id=%s", (total_cost, batch_id))

        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error creating supply batch:", e)
        conn.rollback()
        conn.close()
        return False


def get_all_batches(status=None):
    """Fetch all supply batches (optionally filtered by status)"""
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    if status and status != "All":
        cursor.execute("""
            SELECT sb.*, v.vendor_name 
            FROM supply_batch sb
            JOIN vendor v ON sb.vendor_id = v.vendor_id
            WHERE sb.status = %s
            ORDER BY sb.delivery_date DESC
        """, (status,))
    else:
        cursor.execute("""
            SELECT sb.*, v.vendor_name 
            FROM supply_batch sb
            JOIN vendor v ON sb.vendor_id = v.vendor_id
            ORDER BY sb.delivery_date DESC
        """)
    batches = cursor.fetchall()
    conn.close()
    return batches


def get_batch_items(batch_id):
    """Fetch items (books) in a supply batch"""
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT sbi.*, b.title, b.author
        FROM supply_batch_items sbi
        JOIN books b ON sbi.b_Id = b.b_Id
        WHERE sbi.batch_id = %s
    """, (batch_id,))
    items = cursor.fetchall()
    conn.close()
    return items


# ======================================================
#               ADMIN APPROVAL ACTIONS
# ======================================================

def approve_batch(batch_id, remark):
    """Approve a batch and update stock"""
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # Fetch batch items
        cursor.execute("SELECT b_Id, quantity FROM supply_batch_items WHERE batch_id=%s", (batch_id,))
        items = cursor.fetchall()

        # Increase book stock for each supplied item
        for b_Id, quantity in items:
            cursor.execute("""
                UPDATE books
                SET available_stock = available_stock + %s, total_stock = total_stock + %s
                WHERE b_Id = %s
            """, (quantity, quantity, b_Id))

        # Mark batch as Approved
        cursor.execute("""
            UPDATE supply_batch
            SET status='Approved', admin_remark=%s
            WHERE batch_id=%s
        """, (remark, batch_id))

        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error approving batch:", e)
        conn.rollback()
        conn.close()
        return False


def reject_batch(batch_id, remark):
    """Reject a batch with remark"""
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE supply_batch
            SET status='Rejected', admin_remark=%s
            WHERE batch_id=%s
        """, (remark, batch_id))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error rejecting batch:", e)
        conn.rollback()
        conn.close()
        return False
