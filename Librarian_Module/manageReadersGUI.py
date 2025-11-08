# Librarian_Module/manageReadersGUI.py
from customtkinter import *
from tkinter import messagebox
from Librarian_Module.manageReadersFunctionality import (
    get_all_readers, get_reader_details, update_reader_remark, clear_overdue_fines
)
from datetime import datetime

set_appearance_mode("dark")

class ManageReadersGUI:
    def __init__(self):
        self.root = CTk()
        self.root.title("Manage Readers")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)

        # Title
        CTkLabel(self.root, text="👥 Manage Readers", font=("Arial", 22, "bold")).pack(pady=12)

        # Top frame: search + refresh + back
        top_frame = CTkFrame(self.root)
        top_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.search_var = StringVar()
        self.search_entry = CTkEntry(top_frame, textvariable=self.search_var, width=400, placeholder_text="Search by name or email...")
        self.search_entry.pack(side="left", padx=(0,10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_readers())

        CTkButton(top_frame, text="🔄 Refresh", width=120, command=self.refresh_readers).pack(side="left", padx=6)
        CTkButton(top_frame, text="⬅ Back", width=120, command=self.go_back).pack(side="right")

        # Main container
        main_frame = CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left: readers list
        self.left_frame = CTkFrame(main_frame, width=420, corner_radius=10)
        self.left_frame.pack(side="left", fill="y", padx=(0,10), pady=5)
        self.left_frame.pack_propagate(False)

        CTkLabel(self.left_frame, text="Readers", font=("Arial", 18, "bold")).pack(pady=(8,6))

        self.list_frame = CTkScrollableFrame(self.left_frame, width=400, height=480, corner_radius=10)
        self.list_frame.pack(padx=8, pady=6, fill="both", expand=True)

        # Right: details / actions
        self.right_frame = CTkFrame(main_frame, corner_radius=10)
        self.right_frame.pack(side="left", fill="both", expand=True, pady=5)

        CTkLabel(self.right_frame, text="Reader Details", font=("Arial", 18, "bold")).pack(pady=(8,6))

        self.details_text = CTkTextbox(self.right_frame, width=520, height=260, state="disabled")
        self.details_text.pack(padx=10, pady=6)

        # Remark edit
        CTkLabel(self.right_frame, text="Edit Remark:", font=("Arial", 14, "bold")).pack(pady=(6,2))
        self.remark_entry = CTkEntry(self.right_frame, width=480)
        self.remark_entry.pack(padx=10, pady=(0,8))

        action_frame = CTkFrame(self.right_frame)
        action_frame.pack(pady=8)

        CTkButton(action_frame, text="💾 Save Remark", width=140, command=self.save_remark).grid(row=0, column=0, padx=10)
        CTkButton(action_frame, text="🧾 Clear Fines", width=140, command=self.clear_fines).grid(row=0, column=1, padx=10)
        CTkButton(action_frame, text="🔁 Refresh Details", width=140, command=self.refresh_details).grid(row=0, column=2, padx=10)

        # load readers
        self.readers = []
        self.selected_reader_id = None
        self.refresh_readers()

        self.root.mainloop()

    # ---------------- Load / Refresh Readers ----------------
    def refresh_readers(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.readers = get_all_readers()
        if not self.readers:
            CTkLabel(self.list_frame, text="No readers found.", font=("Arial", 14, "italic")).pack(pady=20)
            return

        for r in self.readers:
            text = f"{r['name']} • Loans: {r['current_loan_count']} • Fines: {r['overdue_fines']:.2f}"
            btn = CTkButton(self.list_frame, text=text, width=360, height=44, anchor="w",
                            command=lambda uid=r['u_Id']: self.select_reader(uid))
            btn.pack(pady=6, padx=8)

    # ---------------- Filter ----------------
    def filter_readers(self):
        q = self.search_var.get().lower()
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        filtered = [r for r in self.readers if q in r['name'].lower() or q in (r.get('email') or '').lower()]
        if not filtered:
            CTkLabel(self.list_frame, text="No matching readers.", font=("Arial", 14, "italic")).pack(pady=20)
            return
        for r in filtered:
            text = f"{r['name']} • Loans: {r['current_loan_count']} • Fines: {r['overdue_fines']:.2f}"
            btn = CTkButton(self.list_frame, text=text, width=360, height=44, anchor="w",
                            command=lambda uid=r['u_Id']: self.select_reader(uid))
            btn.pack(pady=6, padx=8)

    # ---------------- Select ----------------
    def select_reader(self, u_Id):
        self.selected_reader_id = u_Id
        self.show_reader_details()

    # ---------------- Show details ----------------
    def show_reader_details(self):
        if not self.selected_reader_id:
            messagebox.showwarning("Warning", "Select a reader first.")
            return
        reader = get_reader_details(self.selected_reader_id)
        if not reader:
            messagebox.showerror("Error", "Could not fetch reader details.")
            return

        # Show in textbox
        self.details_text.configure(state="normal")
        self.details_text.delete("0.0", "end")

        lines = []
        lines.append(f"Name: {reader.get('name')}")
        lines.append(f"Email: {reader.get('email')}")
        lines.append(f"Phone: {reader.get('phone')}")
        lines.append(f"Date Joined: {reader.get('date_joined')}")
        lines.append(f"Current Loans: {reader.get('current_loan_count')}")
        lines.append(f"Overdue Fines: {float(reader.get('overdue_fines') or 0):.2f}")
        lines.append("")
        lines.append("Active Loans:")
        if reader.get('active_loans'):
            for loan in reader['active_loans']:
                issue = loan['issue_date'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(loan.get('issue_date'), datetime) else str(loan.get('issue_date'))
                due = loan['due_date'].strftime('%Y-%m-%d') if isinstance(loan.get('due_date'), datetime) else str(loan.get('due_date'))
                lines.append(f" - {loan['title']} by {loan['author']} (Issued: {issue}, Due: {due})")
        else:
            lines.append(" - None")

        lines.append("")
        lines.append("Recent Loans (last 10):")
        if reader.get('recent_loans'):
            for loan in reader['recent_loans']:
                issue = loan['issue_date'].strftime('%Y-%m-%d') if isinstance(loan.get('issue_date'), datetime) else str(loan.get('issue_date'))
                status = loan.get('loan_status')
                fine = float(loan.get('fine_amount') or 0)
                lines.append(f" - {loan['title']} ({status}, Issue: {issue}, Fine: {fine:.2f})")
        else:
            lines.append(" - None")

        self.details_text.insert("0.0", "\n".join(lines))
        self.details_text.configure(state="disabled")

        # populate remark entry
        self.remark_entry.delete(0, "end")
        self.remark_entry.insert(0, reader.get('user_remark') or "")

    # ---------------- Save remark ----------------
    def save_remark(self):
        if not self.selected_reader_id:
            messagebox.showwarning("Warning", "Select a reader first.")
            return
        remark = self.remark_entry.get().strip()
        success = update_reader_remark(self.selected_reader_id, remark)
        if success:
            messagebox.showinfo("Success", "Remark updated successfully.")
            self.refresh_readers()
            self.show_reader_details()
        else:
            messagebox.showerror("Error", "Failed to update remark.")

    # ---------------- Clear fines ----------------
    def clear_fines(self):
        if not self.selected_reader_id:
            messagebox.showwarning("Warning", "Select a reader first.")
            return
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear overdue fines for this reader?")
        if not confirm:
            return
        success = clear_overdue_fines(self.selected_reader_id)
        if success:
            messagebox.showinfo("Success", "Overdue fines cleared.")
            self.refresh_readers()
            self.show_reader_details()
        else:
            messagebox.showerror("Error", "Failed to clear fines.")

    def refresh_details(self):
        if not self.selected_reader_id:
            messagebox.showwarning("Warning", "Select a reader first.")
            return
        self.show_reader_details()

    # ---------------- Back ----------------
    def go_back(self):
        from Librarian_Module.librarianGUI import LibrarianGUI
        self.root.destroy()
        LibrarianGUI()
