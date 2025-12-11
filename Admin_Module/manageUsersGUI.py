# Admin_Module/manageUsersGUI.py
from decimal import Decimal
from customtkinter import *
from tkinter import messagebox
from typing import Dict, List

from Admin_Module.manageUsersFunctionality import (
    get_all_users, get_user_by_id, update_user, delete_user
)

set_appearance_mode("dark")


class ManageUsersGUI:
    def __init__(self, u_Id=None):
        self.u_Id = u_Id
        self.root = CTk()
        self.root.title("Manage Users")
        self.root.geometry("950x600")
        self.root.resizable(False, False)

        # Main container
        self.main_frame = CTkFrame(self.root, corner_radius=12)
        self.main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Header row: title + back + search + spacing for actions
        header = CTkFrame(self.main_frame)
        header.pack(fill="x", pady=(0, 8))

        CTkLabel(header, text="Manage Users", font=("Arial", 22, "bold")).pack(side="left", padx=(6, 0))

        right_actions = CTkFrame(header)
        right_actions.pack(side="right", padx=(0, 6))

        CTkButton(right_actions, text="⬅ Back", width=120, command=self.go_back).pack(side="right", padx=(6, 0))

        # Search row
        search_row = CTkFrame(self.main_frame)
        search_row.pack(fill="x", pady=(0, 10), padx=(6, 6))

        self.search_var = StringVar()
        self.search_entry = CTkEntry(
            search_row,
            textvariable=self.search_var,
            placeholder_text="Search users by name or email...",
            width=700,
            height=36,
            font=("Arial", 14)
        )
        self.search_entry.pack(side="left", padx=(6, 8), pady=2, fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_users())

        search_icon = CTkLabel(search_row, text="🔍", font=("Arial", 18))
        search_icon.pack(side="right", padx=(0, 8))

        # Scrollable list of users
        self.scroll_frame = CTkScrollableFrame(self.main_frame, corner_radius=12)
        self.scroll_frame.pack(fill="both", expand=True, padx=6, pady=6)

        # initial load
        self.load_users()

        self.root.mainloop()

    def go_back(self):
        try:
            from Admin_Module.adminGUI import AdminGUI
            self.root.destroy()
            AdminGUI(self.u_Id)
        except Exception as e:
            messagebox.showerror("Error", f"Could not go back: {e}", parent=self.root)

    def load_users(self):
        # Clear existing children
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        raw = get_all_users() or []

        # --- keep GUI-side admin filter as extra safety ---
        raw = [u for u in raw if (u.get("role") or "").lower() != "admin"]

        query = (self.search_var.get() or "").strip().lower()
        if query:
            users = [u for u in raw if
                     (u.get("name") or "").lower().find(query) != -1 or (u.get("email") or "").lower().find(
                         query) != -1]
        else:
            users = raw

        if not users:
            CTkLabel(self.scroll_frame, text="No users found.", font=("Arial", 16)).pack(pady=20)
            return

        for user in users:
            row = CTkFrame(self.scroll_frame, corner_radius=12, fg_color="gray")
            row.pack(fill="x", padx=10, pady=8)

            left = CTkFrame(row, fg_color="gray")
            left.pack(side="left", fill="both", padx=10, pady=10, expand=True)

            # Name as title
            title_label = CTkLabel(
                left,
                text=user.get("name", "Unnamed"),
                font=("Arial", 18, "bold"),
                anchor="w",
                justify="left"
            )
            title_label.pack(fill="x", padx=10, pady=(4, 2))

            # Info lines (one per line)
            info_parts = [
                f"Email: {user.get('email', '-')}",
                f"Role: {user.get('role', '-')}",
                f"Date of Birth: {user.get('date_of_birth') or '-'}",
                f"Phone: {user.get('phone') or '-'}",
                f"Joined: {user.get('date_joined') or '-'}",
                f"Current Loans: {user.get('current_loan_count', 0)}",
                f"Overdue Fines: ₹{user.get('overdue_fines', 0.0)}",
                f"Remark: {user.get('user_remark') or '-'}"
            ]
            info_text = "\n".join(info_parts)
            meta_label = CTkLabel(left, text=info_text, font=("Arial", 13), anchor="w", justify="left")
            meta_label.pack(fill="x", padx=12, pady=(0, 2))

            btns = CTkFrame(row, fg_color="gray")
            btns.pack(side="right", padx=12, pady=12)

            manage_btn = CTkButton(btns, text="Manage User", width=140,
                                   command=lambda u_id=user['u_Id']: self.open_manage_user(u_id))
            manage_btn.pack(pady=(0, 6))
            del_btn = CTkButton(btns, text="Delete", width=100, fg_color="#b22222", hover_color="#9a1a1a",
                                command=lambda u_id=user['u_Id'], name=user.get('name'): self.delete_user_confirm(u_id,
                                                                                                                  name))
            del_btn.pack(fill="both")

    def open_manage_user(self, u_Id: int):
        user = get_user_by_id(u_Id)
        if not user:
            messagebox.showerror("Error", "Could not fetch user details.", parent=self.root)
            return
        ManageUserDetailWindow(self, user)

    def delete_user_confirm(self, u_Id: int, name: str):
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'? This cannot be undone.", parent=self.root):
            return
        success, err = delete_user(u_Id)
        if success:
            messagebox.showinfo("Deleted", "User deleted successfully.", parent=self.root)
            self.load_users()
        else:
            messagebox.showerror("Delete Failed", f"Could not delete user:\n{err}", parent=self.root)


class ManageUserDetailWindow:
    def __init__(self, parent_gui: ManageUsersGUI, user: Dict):
        self.parent = parent_gui
        self.user = user

        # Create modal Toplevel so parent remains
        self.win = CTkToplevel(self.parent.root)
        self.win.title(f"Edit: {user.get('name')}")
        self.win.geometry("700x520")
        self.win.resizable(False, False)

        # Make sure this window stays on top and grabs focus
        try:
            self.win.attributes("-topmost", True)
        except Exception:
            pass
        self.win.focus_force()
        self.win.grab_set()

        container = CTkFrame(self.win, corner_radius=12)
        container.pack(fill="both", expand=True, padx=12, pady=12)

        CTkLabel(container, text="Edit User Details", font=("Arial", 20, "bold")).pack(pady=(4, 8))

        form = CTkFrame(container)
        form.pack(fill="both", expand=True, padx=6, pady=6)

        # helper for aligned fields: label left, entry right
        def add_field(label_text, initial_value, row_no, width=420):
            lbl = CTkLabel(form, text=label_text, font=("Arial", 13))
            lbl.grid(row=row_no, column=0, sticky="w", padx=(6, 6), pady=(8, 2))
            ent = CTkEntry(form, width=width)
            ent.grid(row=row_no, column=1, sticky="w", padx=(6, 6), pady=(8, 2))
            ent.insert(0, "" if initial_value is None else str(initial_value))
            return ent

        # Fields: Users + Reader/Librarian/Vendor normalized fields
        self.name_ent = add_field("Full Name", user.get("name"), 0)
        self.email_ent = add_field("Email", user.get("email"), 1)
        self.role_ent = add_field("Role (Reader/Librarian/Vendor/Admin)", user.get("role"), 2)
        self.dob_ent = add_field("Date of Birth (YYYY-MM-DD)", user.get("date_of_birth") or "", 3)
        self.phone_ent = add_field("Phone", user.get("phone") or "", 4)
        self.remark_ent = add_field("Remark", user.get("user_remark") or "", 5)
        self.current_loans_ent = add_field("Current Loan Count", user.get("current_loan_count") or 0, 6)
        self.overdue_fines_ent = add_field("Overdue Fines (₹)", user.get("overdue_fines") or 0.0, 7)

        btn_frame = CTkFrame(container)
        btn_frame.pack(fill="x", pady=(10, 0), padx=6)

        save_btn = CTkButton(btn_frame, text="Save", width=140, command=self.save_changes)
        save_btn.pack(side="right", padx=(8, 12))

        cancel_btn = CTkButton(btn_frame, text="Cancel", width=120, command=self.close)
        cancel_btn.pack(side="right", padx=(8, 0))

    def close(self):
        try:
            if self.win.winfo_exists():
                self.win.destroy()
        except Exception:
            pass

    def save_changes(self):
        data = {}
        name = self.name_ent.get().strip()
        email = self.email_ent.get().strip()
        role = self.role_ent.get().strip()
        dob = self.dob_ent.get().strip() or None
        phone = self.phone_ent.get().strip() or None
        remark = self.remark_ent.get().strip() or None

        # validations
        if not name or not email:
            messagebox.showerror("Validation Error", "Name and email are required.", parent=self.win)
            return

        data["name"] = name
        data["email"] = email
        data["role"] = role or "Reader"
        data["date_of_birth"] = dob

        data["phone"] = phone
        data["user_remark"] = remark

        # numeric fields
        try:
            curr = int(self.current_loans_ent.get().strip())
            if curr < 0:
                raise ValueError("current loans must be >= 0")
            data["current_loan_count"] = curr
        except Exception as e:
            messagebox.showerror("Validation Error", f"Current loan count invalid:\n{e}", parent=self.win)
            return

        try:
            fines = Decimal(self.overdue_fines_ent.get().strip())
            if fines < 0:
                raise ValueError("overdue fines must be >= 0")
            data["overdue_fines"] = float(fines)
        except Exception as e:
            messagebox.showerror("Validation Error", f"Overdue fines invalid:\n{e}", parent=self.win)
            return

        success, err = update_user(self.user["u_Id"], data)
        if success:
            messagebox.showinfo("Success", "User updated successfully.", parent=self.win)
            try:
                self.parent.load_users()
            except Exception:
                pass
            self.close()
        else:
            messagebox.showerror("Database Error", f"Failed to update user:\n{err}", parent=self.win)
