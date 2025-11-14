# Librarian_Module/loanRecordsGUI.py
from customtkinter import *
from tkinter import messagebox
from datetime import datetime
from Librarian_Module.loanRecordsFunctionality import (
    get_all_loans, issue_book, mark_as_returned
)

set_appearance_mode("dark")


class LoanRecordsGUI:
    def __init__(self, u_Id):
        self.u_Id = u_Id
        self.root = CTk()
        self.root.title("🧾 Loan Records")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)

        CTkLabel(self.root, text="📘 Manage Loan Records", font=("Arial", 24, "bold")).pack(pady=20)

        # --------- Top Buttons ---------
        top_frame = CTkFrame(self.root)
        top_frame.pack(fill="x", padx=20, pady=10)

        self.filter_var = StringVar(value="All")
        filter_menu = CTkOptionMenu(
            top_frame,
            variable=self.filter_var,
            values=["All", "Active", "Overdue", "Returned", "Lost"],
            command=lambda _: self.load_loans()
        )
        filter_menu.pack(side="left", padx=10)

        CTkButton(top_frame, text="➕ Issue New Book", width=160, command=self.issue_window).pack(side="left", padx=10)
        CTkButton(top_frame, text="🔄 Refresh", width=120, command=self.load_loans).pack(side="left", padx=10)
        CTkButton(top_frame, text="⬅ Back", width=120, command=self.go_back).pack(side="right", padx=10)

        # --------- Loan List ---------
        self.scroll_frame = CTkScrollableFrame(self.root, width=950, height=450)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.load_loans()
        self.root.mainloop()

    # --------- Load Loans ---------
    def load_loans(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        filter_choice = self.filter_var.get()
        loans = get_all_loans(filter_choice)

        if not loans:
            CTkLabel(self.scroll_frame, text="No records found.", font=("Arial", 14, "italic")).pack(pady=20)
            return

        for l in loans:
            issue = l["issue_date"].strftime("%Y-%m-%d")
            due = l["due_date"].strftime("%Y-%m-%d")
            ret = l["return_date"].strftime("%Y-%m-%d") if l["return_date"] else "—"

            text = (f"👤 {l['reader_name']} | 📖 {l['title']} by {l['author']}\n"
                    f"Issue: {issue} | Due: {due} | Return: {ret} | Status: {l['loan_status']}")

            frame = CTkFrame(self.scroll_frame, corner_radius=10)
            frame.pack(fill="x", pady=6, padx=10)

            CTkLabel(frame, text=text, font=("Arial", 14), justify="left").pack(side="left", padx=10)
            if l["loan_status"] == "Active":
                CTkButton(frame, text="✅ Mark Returned", width=150,
                          command=lambda lid=l["loan_id"]: self.return_book(lid)).pack(side="right", padx=10)

    # --------- Mark as Returned ---------
    def return_book(self, loan_id):
        confirm = messagebox.askyesno("Confirm", "Mark this book as returned?")
        if not confirm:
            return

        if mark_as_returned(loan_id):
            messagebox.showinfo("Success", "Book marked as returned!")
            self.load_loans()
        else:
            messagebox.showerror("Error", "Failed to update loan status.")

    # --------- Issue Book Window ---------
    def issue_window(self):
        from Librarian_Module.loanRecordsFunctionality import get_connection
        conn = get_connection()
        if not conn:
            return
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT u_Id, name FROM users WHERE role='Reader';")
        readers = cursor.fetchall()
        cursor.execute("SELECT b_Id, title FROM books WHERE available_stock > 0;")
        books = cursor.fetchall()
        conn.close()

        win = CTkToplevel(self.root)
        win.title("Issue New Book")
        win.geometry("400x400")

        CTkLabel(win, text="Select Reader:", font=("Arial", 14)).pack(pady=(15, 5))
        reader_var = StringVar(value=f"{readers[0]['u_Id']} - {readers[0]['name']}" if readers else "")
        reader_menu = CTkOptionMenu(win, variable=reader_var,
                                    values=[f"{r['u_Id']} - {r['name']}" for r in readers])
        reader_menu.pack(pady=5)

        CTkLabel(win, text="Select Book:", font=("Arial", 14)).pack(pady=(15, 5))
        book_var = StringVar(value=f"{books[0]['b_Id']} - {books[0]['title']}" if books else "")
        book_menu = CTkOptionMenu(win, variable=book_var,
                                  values=[f"{b['b_Id']} - {b['title']}" for b in books])
        book_menu.pack(pady=5)

        def issue_now():
            if not readers or not books:
                messagebox.showerror("Error", "No readers or books available.")
                return
            u_Id = int(reader_var.get().split(" - ")[0])
            b_Id = int(book_var.get().split(" - ")[0])

            if issue_book(u_Id, b_Id):
                messagebox.showinfo("Success", "Book issued successfully!")
                win.destroy()
                self.load_loans()
            else:
                messagebox.showerror("Error", "Failed to issue book.")

        CTkButton(win, text="💾 Issue", width=150, command=issue_now).pack(pady=25)

    # --------- Back ---------
    def go_back(self):
        from Librarian_Module.librarianGUI import LibrarianGUI
        self.root.destroy()
        LibrarianGUI(self.u_Id)
