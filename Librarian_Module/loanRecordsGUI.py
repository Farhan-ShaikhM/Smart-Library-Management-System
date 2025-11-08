# Librarian_Module/loanRecordsGUI.py
from customtkinter import *
from tkinter import messagebox
from datetime import datetime
from Librarian_Module.loanRecordsFunctionality import (
    get_all_loans,
    update_loan_status,
    get_overdue_loans,
    increment_book_stock,
)

set_appearance_mode("dark")

class LoanRecordsGUI:
    def __init__(self):
        self.root = CTk()
        self.root.title("🧾 Loan Records Management")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)

        # ---------------- Title ----------------
        CTkLabel(self.root, text="📚 Loan Records Management", font=("Arial", 22, "bold")).pack(pady=15)

        # ---------------- Filter + Buttons ----------------
        control_frame = CTkFrame(self.root)
        control_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.filter_var = StringVar(value="All")
        filter_menu = CTkOptionMenu(
            control_frame,
            variable=self.filter_var,
            values=["All", "Active", "Overdue", "Returned - On Time", "Returned - Late", "Lost"],
            width=200,
            command=self.filter_loans
        )
        filter_menu.pack(side="left", padx=10)

        CTkButton(control_frame, text="🔄 Refresh", width=120, command=self.refresh_loans).pack(side="left", padx=10)
        CTkButton(control_frame, text="⬅ Back", width=120, command=self.go_back).pack(side="right", padx=10)

        # ---------------- Scrollable Area ----------------
        self.scroll_frame = CTkScrollableFrame(self.root, width=950, height=450, corner_radius=15)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # ---------------- Action Buttons ----------------
        action_frame = CTkFrame(self.root)
        action_frame.pack(pady=10)
        CTkButton(action_frame, text="✅ Mark Returned", width=180, command=self.mark_returned).grid(row=0, column=0, padx=10)
        CTkButton(action_frame, text="❌ Mark Lost", width=180, command=self.mark_lost).grid(row=0, column=1, padx=10)

        # ---------------- Load Data ----------------
        self.selected_loan = None
        self.loans = []
        self.refresh_loans()

        self.root.mainloop()

    # ---------------- Refresh Loan List ----------------
    def refresh_loans(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        selected_filter = self.filter_var.get()
        if selected_filter == "Overdue":
            self.loans = get_overdue_loans()
        else:
            self.loans = get_all_loans(selected_filter)

        if not self.loans:
            CTkLabel(self.scroll_frame, text="No loan records found.", font=("Arial", 16, "italic")).pack(pady=20)
            return

        for loan in self.loans:
            issue_date = loan["issue_date"].strftime("%Y-%m-%d") if isinstance(loan["issue_date"], datetime) else str(loan["issue_date"])
            due_date = loan["due_date"].strftime("%Y-%m-%d") if isinstance(loan["due_date"], datetime) else str(loan["due_date"])
            return_date = loan["return_date"].strftime("%Y-%m-%d") if loan["return_date"] else "—"

            btn_text = (
                f"{loan['reader_name']} borrowed '{loan['title']}' by {loan['author']}\n"
                f"Issue: {issue_date} | Due: {due_date} | Return: {return_date} | "
                f"Fine: ₹{loan['fine_amount']:.2f} | Status: {loan['loan_status']}"
            )

            btn = CTkButton(
                self.scroll_frame,
                text=btn_text,
                width=900,
                height=65,
                anchor="w",
                font=("Arial", 14),
                command=lambda l=loan: self.select_loan(l)
            )
            btn.pack(pady=6, padx=10)

    # ---------------- Select Loan ----------------
    def select_loan(self, loan):
        self.selected_loan = loan
        messagebox.showinfo("Selected", f"Selected Loan:\n'{loan['title']}' by {loan['author']}'\nReader: {loan['reader_name']}")

    # ---------------- Mark Returned ----------------
    def mark_returned(self):
        if not self.selected_loan:
            messagebox.showwarning("Warning", "Select a loan first.")
            return

        confirm = messagebox.askyesno("Confirm", "Mark this loan as Returned?")
        if not confirm:
            return

        # Fine Calculation
        due_date = self.selected_loan["due_date"]
        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

        days_overdue = max((datetime.now().date() - due_date).days, 0)
        daily_fine = float(self.selected_loan.get("daily_late_fine", 10.0))
        fine = days_overdue * daily_fine
        status = "Returned - On Time" if days_overdue == 0 else "Returned - Late"

        success = update_loan_status(self.selected_loan["loan_id"], status, fine)
        if success:
            increment_book_stock(self.selected_loan["b_Id"])  # return stock
            messagebox.showinfo("Success", f"Book marked as {status}.\nFine: ₹{fine:.2f}")
            self.refresh_loans()
        else:
            messagebox.showerror("Error", "Failed to update loan status.")

    # ---------------- Mark Lost ----------------
    def mark_lost(self):
        if not self.selected_loan:
            messagebox.showwarning("Warning", "Select a loan first.")
            return

        confirm = messagebox.askyesno("Confirm", "Mark this book as Lost?")
        if not confirm:
            return

        fine = float(self.selected_loan.get("fine_amount", 0)) or 0.0
        success = update_loan_status(self.selected_loan["loan_id"], "Lost", fine)
        if success:
            messagebox.showinfo("Success", "Book marked as Lost successfully.")
            self.refresh_loans()
        else:
            messagebox.showerror("Error", "Failed to mark as lost.")

    # ---------------- Filter ----------------
    def filter_loans(self, *args):
        self.refresh_loans()

    # ---------------- Back ----------------
    def go_back(self):
        from Librarian_Module.librarianGUI import LibrarianGUI
        self.root.destroy()
        LibrarianGUI()
