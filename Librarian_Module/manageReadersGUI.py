# Librarian_Module/manageReadersGUI.py
from customtkinter import *
from tkinter import messagebox
from Librarian_Module.manageReadersFunctionality import (
    get_all_readers, update_reader, delete_reader
)
from datetime import datetime

set_appearance_mode("dark")


class ManageReadersGUI:
    def __init__(self, u_Id):
        self.u_Id = u_Id
        self.root = CTk()
        self.root.title("👥 Manage Readers")
        self.root.geometry("950x650")
        self.root.resizable(False, False)

        CTkLabel(self.root, text="👥 Manage Readers", font=("Arial", 24, "bold")).pack(pady=20)
        CTkButton(self.root, text="⬅ Back", width=150, command=self.go_back).pack(pady=5)

        # ---------- Reader List ----------
        self.scroll_frame = CTkScrollableFrame(self.root, width=900, height=500)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.load_readers()
        self.root.mainloop()

    # ---------- Load Readers ----------
    def load_readers(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        readers = get_all_readers()
        if not readers:
            CTkLabel(self.scroll_frame, text="No readers found.", font=("Arial", 14, "italic")).pack(pady=20)
            return

        for r in readers:
            info = (f"👤 {r['name']} | 📧 {r['email'] or 'N/A'}\n"
                    f"DOB: {r['date_of_birth'] or 'N/A'} | ID: {r['u_Id']}")

            frame = CTkFrame(self.scroll_frame, corner_radius=10)
            frame.pack(fill="x", pady=5, padx=10)

            CTkLabel(frame, text=info, font=("Arial", 14), justify="left").pack(side="left", padx=10)

            CTkButton(frame, text="✏ Edit", width=100, command=lambda uid=r["u_Id"]: self.edit_reader(uid)).pack(side="right", padx=5)
            CTkButton(frame, text="🗑 Delete", width=100, fg_color="red", command=lambda uid=r["u_Id"]: self.remove_reader(uid)).pack(side="right", padx=5)

    # ---------- Edit Reader ----------
    def edit_reader(self, u_Id):
        import mysql.connector
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="slms_db")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE u_Id=%s AND role='Reader';", (u_Id,))
        r = cursor.fetchone()
        conn.close()

        if not r:
            messagebox.showerror("Error", "Reader not found.")
            return

        win = CTkToplevel(self.root)
        win.title("Edit Reader")
        win.geometry("400x400")

        CTkLabel(win, text="Name:", font=("Arial", 14)).pack(pady=(10, 0))
        name_entry = CTkEntry(win, width=300)
        name_entry.insert(0, r["name"])
        name_entry.pack(pady=5)

        CTkLabel(win, text="Email:", font=("Arial", 14)).pack(pady=(10, 0))
        email_entry = CTkEntry(win, width=300)
        email_entry.insert(0, r["email"])
        email_entry.pack(pady=5)

        CTkLabel(win, text="Date of Birth (YYYY-MM-DD):", font=("Arial", 14)).pack(pady=(10, 0))
        dob_entry = CTkEntry(win, width=300)
        dob_entry.insert(0, str(r["date_of_birth"]) if r["date_of_birth"] else "")
        dob_entry.pack(pady=5)

        def save_changes():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            dob = dob_entry.get().strip()

            try:
                if dob:
                    datetime.strptime(dob, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD).")
                return

            if update_reader(u_Id, name, email, dob):
                messagebox.showinfo("Success", "Reader updated successfully!")
                win.destroy()
                self.load_readers()
            else:
                messagebox.showerror("Error", "Failed to update reader.")

        CTkButton(win, text="💾 Save Changes", command=save_changes).pack(pady=20)

    # ---------- Delete Reader ----------
    def remove_reader(self, u_Id):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this reader?")
        if not confirm:
            return

        if delete_reader(u_Id):
            messagebox.showinfo("Success", "Reader deleted successfully.")
            self.load_readers()
        else:
            messagebox.showerror("Error", "Failed to delete reader.")

    # ---------- Back ----------
    def go_back(self):
        from Librarian_Module.librarianGUI import LibrarianGUI
        self.root.destroy()
        LibrarianGUI(self.u_Id)
