# Librarian_Module/librarianGUI.py
from customtkinter import *
from tkinter import messagebox
from Librarian_Module.librarianFunctionality import get_librarian_summary

set_appearance_mode("dark")


class LibrarianGUI:
    """Main dashboard for Librarian users."""

    def __init__(self, u_Id):
        self.u_Id = u_Id
        self.root = CTk()
        self.root.title("📚 Librarian Dashboard")
        self.root.geometry("950x600")
        self.root.resizable(False, False)

        # ------------- HEADER -------------
        CTkLabel(
            self.root,
            text="📘 Librarian Dashboard",
            font=("Arial", 26, "bold"),
        ).pack(pady=20)

        # summary frame
        summary = get_librarian_summary(self.u_Id)
        stats_frame = CTkFrame(self.root, corner_radius=15)
        stats_frame.pack(padx=20, pady=10, fill="x")

        CTkLabel(
            stats_frame,
            text=f"Total Books: {summary.get('total_books',0)}",
            font=("Arial", 16),
        ).pack(side="left", padx=25, pady=10)
        CTkLabel(
            stats_frame,
            text=f"Readers: {summary.get('total_readers',0)}",
            font=("Arial", 16),
        ).pack(side="left", padx=25, pady=10)
        CTkLabel(
            stats_frame,
            text=f"Active Loans: {summary.get('active_loans',0)}",
            font=("Arial", 16),
        ).pack(side="left", padx=25, pady=10)

        # ------------- MAIN BUTTONS -------------
        main_frame = CTkFrame(self.root)
        main_frame.pack(expand=True, pady=20)

        btn_w, btn_h = 300, 60
        CTkButton(
            main_frame,
            text="📚 Manage Books",
            width=btn_w,
            height=btn_h,
            font=("Arial", 16, "bold"),
            command=self.manage_books,
        ).pack(pady=10)

        CTkButton(
            main_frame,
            text="👥 Manage Readers",
            width=btn_w,
            height=btn_h,
            font=("Arial", 16, "bold"),
            command=self.manage_readers,
        ).pack(pady=10)

        CTkButton(
            main_frame,
            text="🧾 Loan Records",
            width=btn_w,
            height=btn_h,
            font=("Arial", 16, "bold"),
            command=self.loan_records,
        ).pack(pady=10)

        CTkButton(
            main_frame,
            text="📘 Request New Books",
            width=btn_w,
            height=btn_h,
            font=("Arial", 16, "bold"),
            command=self.request_books,
        ).pack(pady=10)

        # ------------- FOOTER -------------
        CTkButton(
            self.root,
            text="⬅ Logout",
            width=200,
            command=self.logout,
        ).pack(pady=25)

        self.root.mainloop()

    # --------- Navigation Commands ---------
    def manage_books(self):
        from Librarian_Module.manageBooksGUI import ManageBooksGUI
        self.root.destroy()
        ManageBooksGUI(self.u_Id)

    def manage_readers(self):
        from Librarian_Module.manageReadersGUI import ManageReadersGUI
        self.root.destroy()
        ManageReadersGUI(self.u_Id)

    def loan_records(self):
        from Librarian_Module.loanRecordsGUI import LoanRecordsGUI
        self.root.destroy()
        LoanRecordsGUI(self.u_Id)

    def request_books(self):
        from Librarian_Module.requestBooksGUI import RequestBooksGUI
        self.root.destroy()
        RequestBooksGUI(self.u_Id)

    def logout(self):
        from Login_Module.loginGUI import LoginGUI
        self.root.destroy()
        root = CTk()
        LoginGUI(root)
        root.mainloop()
