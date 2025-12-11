import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Tuple, Optional

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "slms_db"
}


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("DB connect error:", e)
        return None


def get_users_by_role(role: str) -> List[Dict]:
    role = (role or "").strip()
    if role not in ("Reader", "Librarian", "Vendor"):
        return []

    conn = get_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        if role == "Reader":
            cursor.execute("""
                SELECT
                  u.u_Id, u.name, u.email, u.role, u.date_of_birth,
                  r.phone AS phone, r.date_joined AS date_joined,
                  COALESCE(r.current_loan_count, 0) AS current_loan_count,
                  COALESCE(r.overdue_fines, 0.0) AS overdue_fines,
                  COALESCE(r.user_remark, '') AS user_remark
                FROM Users u
                LEFT JOIN Reader r ON u.u_Id = r.u_Id
                WHERE u.role = 'Reader'
                ORDER BY u.name
            """)
        elif role == "Librarian":
            cursor.execute("""
                SELECT
                  u.u_Id, u.name, u.email, u.role, u.date_of_birth,
                  l.phone AS phone, l.date_created AS date_joined,
                  0 AS current_loan_count,
                  0.00 AS overdue_fines
                FROM Users u
                LEFT JOIN Librarian l ON u.u_Id = l.u_Id
                WHERE u.role = 'Librarian'
                ORDER BY u.name
            """)
        else:  # Vendor
            # Attempt vendor join — if Vendor table missing or different, return empty list and log.
            try:
                cursor.execute("""
                    SELECT
                      u.u_Id, u.name, u.email, u.role, u.date_of_birth,
                      v.phone AS phone, v.date_joined AS date_joined,
                      0 AS current_loan_count,
                      0.00 AS overdue_fines,
                      COALESCE(v.vendor_remark, '') AS user_remark
                    FROM Users u
                    LEFT JOIN Vendor v ON u.u_Id = v.u_Id
                    WHERE u.role = 'Vendor'
                    ORDER BY u.name
                """)
            except Error as ex:
                print(f"[DEBUG] get_users_by_role(Vendor) query failed: {ex}")
                cursor.close()
                conn.close()
                return []
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows or []
    except Error as e:
        print("get_users_by_role error:", e)
        try:
            conn.close()
        except Exception:
            pass
        return []


def get_all_users() -> List[Dict]:
    users = []
    users.extend(get_users_by_role("Reader"))
    users.extend(get_users_by_role("Librarian"))
    users.extend(get_users_by_role("Vendor"))
    return users


def get_user_by_id(u_Id: int) -> Optional[Dict]:
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT
                    u.u_Id, u.name, u.email, u.role, u.date_of_birth,
                    r.phone AS reader_phone, r.date_joined AS reader_date_joined,
                    r.current_loan_count, r.overdue_fines, r.user_remark AS reader_user_remark,
                    l.phone AS librarian_phone, l.date_created AS librarian_date_created,
                    v.phone AS vendor_phone, v.date_joined AS vendor_date_joined, v.vendor_remark AS vendor_remark
                FROM Users u
                LEFT JOIN Reader r ON u.u_Id = r.u_Id
                LEFT JOIN Librarian l ON u.u_Id = l.u_Id
                LEFT JOIN Vendor v ON u.u_Id = v.u_Id
                WHERE u.u_Id = %s
            """, (u_Id,))
        except Error:
            cursor.execute("""
                SELECT
                    u.u_Id, u.name, u.email, u.role, u.date_of_birth,
                    r.phone AS reader_phone, r.date_joined AS reader_date_joined,
                    r.current_loan_count, r.overdue_fines, r.user_remark AS reader_user_remark,
                    l.phone AS librarian_phone, l.date_created AS librarian_date_created, l.user_remark AS librarian_user_remark,
                    NULL AS vendor_phone, NULL AS vendor_date_joined, NULL AS vendor_remark
                FROM Users u
                LEFT JOIN Reader r ON u.u_Id = r.u_Id
                LEFT JOIN Librarian l ON u.u_Id = l.u_Id
                WHERE u.u_Id = %s
            """, (u_Id,))

        raw = cursor.fetchone()
        cursor.close()
        conn.close()

        if not raw:
            return None

        out = {
            "u_Id": raw.get("u_Id"),
            "name": raw.get("name"),
            "email": raw.get("email"),
            "role": raw.get("role"),
            "date_of_birth": raw.get("date_of_birth"),
            "phone": None,
            "date_joined": None,
            "current_loan_count": int(raw.get("current_loan_count") or 0),
            "overdue_fines": float(raw.get("overdue_fines") or 0.0),
            "user_remark": raw.get("reader_user_remark") or raw.get("librarian_user_remark") or raw.get("vendor_remark") or ""
        }

        role = (out["role"] or "").strip()
        if role == "Reader":
            out["phone"] = raw.get("reader_phone")
            out["date_joined"] = raw.get("reader_date_joined")
            out["user_remark"] = raw.get("reader_user_remark") or ""
        elif role == "Librarian":
            out["phone"] = raw.get("librarian_phone")
            out["date_joined"] = raw.get("librarian_date_created")
            out["current_loan_count"] = 0
            out["overdue_fines"] = 0.0
        elif role == "Vendor":
            out["phone"] = raw.get("vendor_phone")
            out["date_joined"] = raw.get("vendor_date_joined")
            out["current_loan_count"] = 0
            out["overdue_fines"] = 0.0
            out["user_remark"] = raw.get("vendor_remark") or ""
        else:
            # fallback: prefer reader -> librarian -> vendor
            out["phone"] = raw.get("reader_phone") or raw.get("librarian_phone") or raw.get("vendor_phone")
            out["date_joined"] = raw.get("reader_date_joined") or raw.get("librarian_date_created") or raw.get("vendor_date_joined")

        return out
    except Error as e:
        print("get_user_by_id error:", e)
        try:
            conn.close()
        except Exception:
            pass
        return None


def update_user(u_Id: int, user_data: Dict) -> Tuple[bool, Optional[str]]:
    conn = get_connection()
    if conn is None:
        return False, "DB connection failed"

    try:
        cursor = conn.cursor()

        u_fields = []
        u_vals = []
        for k in ("name", "email", "role", "date_of_birth"):
            if k in user_data:
                u_fields.append(f"{k} = %s")
                u_vals.append(user_data[k])
        if u_fields:
            sql = "UPDATE Users SET " + ", ".join(u_fields) + " WHERE u_Id = %s"
            u_vals.append(u_Id)
            cursor.execute(sql, tuple(u_vals))

        effective_role = None
        if "role" in user_data:
            effective_role = (user_data.get("role") or "").strip()
        else:
            cursor.execute("SELECT role FROM Users WHERE u_Id = %s", (u_Id,))
            r = cursor.fetchone()
            if r:
                effective_role = r[0]
        if effective_role is None:
            effective_role = ""

        effective_role = effective_role.strip()

        if effective_role == "Reader":
            r_fields = []
            r_vals = []
            for k in ("phone", "user_remark", "current_loan_count", "overdue_fines"):
                if k in user_data:
                    r_fields.append(f"{k} = %s")
                    r_vals.append(user_data[k])
            if r_fields:
                cursor.execute("SELECT u_Id FROM Reader WHERE u_Id = %s", (u_Id,))
                if cursor.fetchone():
                    sql = "UPDATE Reader SET " + ", ".join(r_fields) + " WHERE u_Id = %s"
                    r_vals.append(u_Id)
                    cursor.execute(sql, tuple(r_vals))
                else:
                    cols = ["u_Id"] + [k for k in ("phone", "user_remark", "current_loan_count", "overdue_fines") if k in user_data]
                    vals = [u_Id] + [user_data[k] for k in ("phone", "user_remark", "current_loan_count", "overdue_fines") if k in user_data]
                    placeholders = ", ".join(["%s"] * len(vals))
                    sql = f"INSERT INTO Reader ({', '.join(cols)}) VALUES ({placeholders})"
                    cursor.execute(sql, tuple(vals))

        elif effective_role == "Librarian":
            l_fields = []
            l_vals = []
            for k in ("phone", "user_remark"):
                if k in user_data:
                    l_fields.append(f"{k} = %s")
                    l_vals.append(user_data[k])
            if l_fields:
                cursor.execute("SELECT u_Id FROM Librarian WHERE u_Id = %s", (u_Id,))
                if cursor.fetchone():
                    sql = "UPDATE Librarian SET " + ", ".join(l_fields) + " WHERE u_Id = %s"
                    l_vals.append(u_Id)
                    cursor.execute(sql, tuple(l_vals))
                else:
                    cols = ["u_Id"] + [k for k in ("phone", "user_remark") if k in user_data]
                    vals = [u_Id] + [user_data[k] for k in ("phone", "user_remark") if k in user_data]
                    placeholders = ", ".join(["%s"] * len(vals))
                    sql = f"INSERT INTO Librarian ({', '.join(cols)}) VALUES ({placeholders})"
                    cursor.execute(sql, tuple(vals))

        elif effective_role == "Vendor":
            v_fields = []
            v_vals = []
            if "phone" in user_data:
                v_fields.append("phone = %s")
                v_vals.append(user_data["phone"])
            if "user_remark" in user_data:
                v_fields.append("vendor_remark = %s")
                v_vals.append(user_data["user_remark"])
            if v_fields:
                cursor.execute("SELECT u_Id FROM Vendor WHERE u_Id = %s", (u_Id,))
                if cursor.fetchone():
                    sql = "UPDATE Vendor SET " + ", ".join(v_fields) + " WHERE u_Id = %s"
                    v_vals.append(u_Id)
                    cursor.execute(sql, tuple(v_vals))
                else:
                    cols = ["u_Id"]
                    vals = [u_Id]
                    if "phone" in user_data:
                        cols.append("phone")
                        vals.append(user_data["phone"])
                    if "user_remark" in user_data:
                        cols.append("vendor_remark")
                        vals.append(user_data["user_remark"])
                    placeholders = ", ".join(["%s"] * len(vals))
                    sql = f"INSERT INTO Vendor ({', '.join(cols)}) VALUES ({placeholders})"
                    cursor.execute(sql, tuple(vals))


        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        try:
            conn.rollback()
            conn.close()
        except Exception:
            pass
        return False, str(e)


def delete_user(u_Id: int) -> Tuple[bool, Optional[str]]:
    conn = get_connection()
    if conn is None:
        return False, "DB connection failed"

    try:
        cursor = conn.cursor()
        blocking = []

        cursor.execute("SELECT COUNT(*) FROM Loan_Record WHERE u_Id = %s", (u_Id,))
        cnt_borrower = cursor.fetchone()[0]
        if cnt_borrower > 0:
            blocking.append(f"Loan_Record (as borrower: {cnt_borrower})")

        cursor.execute("SELECT COUNT(*) FROM Loan_Record WHERE librarian_id = %s", (u_Id,))
        cnt_libr = cursor.fetchone()[0]
        if cnt_libr > 0:
            blocking.append(f"Loan_Record (as librarian: {cnt_libr})")

        cursor.execute("SELECT COUNT(*) FROM Personal_Rating WHERE u_Id = %s", (u_Id,))
        cnt_rating = cursor.fetchone()[0]
        if cnt_rating > 0:
            blocking.append(f"Personal_Rating (ratings: {cnt_rating})")

        if blocking:
            cursor.close()
            conn.close()
            return False, "Cannot delete user — referencing records exist: " + "; ".join(blocking)

        cursor.execute("SELECT role FROM Users WHERE u_Id = %s", (u_Id,))
        row = cursor.fetchone()
        role = row[0] if row else None

        if role == "Reader":
            cursor.execute("DELETE FROM Reader WHERE u_Id = %s", (u_Id,))
        elif role == "Librarian":
            cursor.execute("DELETE FROM Librarian WHERE u_Id = %s", (u_Id,))
        elif role == "Vendor":
            cursor.execute("DELETE FROM Vendor WHERE u_Id = %s", (u_Id,))
        else:
            cursor.execute("DELETE FROM Reader WHERE u_Id = %s", (u_Id,))
            cursor.execute("DELETE FROM Librarian WHERE u_Id = %s", (u_Id,))
            try:
                cursor.execute("DELETE FROM Vendor WHERE u_Id = %s", (u_Id,))
            except Error:
                pass

        cursor.execute("DELETE FROM Users WHERE u_Id = %s", (u_Id,))

        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        try:
            conn.rollback()
            conn.close()
        except Exception:
            pass
        return False, str(e)
