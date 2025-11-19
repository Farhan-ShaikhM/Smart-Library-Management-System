# Librarian_Module/librarianGUI.py
from customtkinter import *
from tkinter import messagebox
from Librarian_Module.librarianFunctionality import get_librarian_summary

set_appearance_mode("dark")


class LibrarianGUI:
    """Modern Librarian Dashboard (UI similar to Reader Module)."""

    def __init__(self, u_Id):
        self.u_Id = u_Id

        # Get summary data
        summary = get_librarian_summary(self.u_Id)
        if not summary:
            messagebox.showerror("Error", "Unable to load librarian data.")
            return

        # ---------------- Main window ----------------
        self.root = CTk()
        self.root.title("Librarian Dashboard")
        self.root.geometry("1050x650")
        self.root.resizable(0, 0)

        # ---------------- Main container ----------------
        self.main_frame = CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ============================================================
        # LEFT SIDEBAR (same pattern as Reader)
        # ============================================================
        self.left_frame = CTkFrame(self.main_frame, width=250, corner_radius=15)
        self.left_frame.pack(side="left", fill="y", padx=(10, 5), pady=10)

        # Librarian Icon + Name
        self.welcome_frame = CTkFrame(self.left_frame, corner_radius=15)
        self.welcome_frame.pack(fill="x", padx=10, pady=10)

        self.lib_logo = CTkLabel(self.welcome_frame, text="🧑‍🏫", font=("Arial", 100))
        self.lib_logo.pack(pady=(20, 10))

        self.welcome_label = CTkLabel(
            self.welcome_frame,
            text="Librarian",
            font=("Arial", 18, "bold"),
            justify="center"
        )
        self.welcome_label.pack(pady=(0, 20))

        # Quick Links (Left Buttons)
        self.manage_books_btn = CTkButton(
            self.left_frame,
            text="📘 Manage Books",
            font=("Arial", 18, "bold"),
            width=180,
            height=40,
            corner_radius=15,
            command=self.manage_books
        )
        self.manage_books_btn.pack(pady=15, padx=20, fill="x")

        self.manage_readers_btn = CTkButton(
            self.left_frame,
            text="👥 Manage Readers",
            font=("Arial", 18, "bold"),
            width=180,
            height=40,
            corner_radius=15,
            command=self.manage_readers
        )
        self.manage_readers_btn.pack(pady=15, padx=20, fill="x")

        self.loan_records_btn = CTkButton(
            self.left_frame,
            text="🧾 Loan Records",
            font=("Arial", 18, "bold"),
            width=180,
            height=40,
            corner_radius=15,
            command=self.loan_records
        )
        self.loan_records_btn.pack(pady=15, padx=20, fill="x")

        self.request_books_btn = CTkButton(
            self.left_frame,
            text="📦 Request Books",
            font=("Arial", 18, "bold"),
            width=180,
            height=40,
            corner_radius=15,
            command=self.request_books
        )
        self.request_books_btn.pack(pady=15, padx=20, fill="x")

        self.logout_btn = CTkButton(
            self.left_frame,
            text="⬅ Logout",
            font=("Arial", 18, "bold"),
            width=180,
            height=40,
            corner_radius=15,
            fg_color="#c0392b",
            command=self.logout
        )
        self.logout_btn.pack(pady=(40, 10), padx=20, fill="x")

        # ============================================================
        # RIGHT CONTENT AREA (Stats + Quick Actions)
        # ============================================================
        self.right_frame = CTkFrame(self.main_frame, corner_radius=15)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

        # ---------------- Stats Section ----------------
        self.stats_frame = CTkFrame(self.right_frame, corner_radius=15)
        self.stats_frame.pack(pady=(10, 20))

        card_size = 150

        # Container for stats cards
        self.stats_container = CTkFrame(self.stats_frame)
        self.stats_container.pack()

        # Total Books Card
        self.books_card = CTkFrame(self.stats_container, width=card_size, height=card_size, corner_radius=15)
        self.books_card.pack(side="left", padx=10)
        self.books_card.pack_propagate(False)
        CTkLabel(
            self.books_card,
            text=f"Total Books\n{summary.get('total_books', 0)}",
            font=("Arial", 16),
            justify="center"
        ).pack(expand=True)

        # Total Readers Card
        self.readers_card = CTkFrame(self.stats_container, width=card_size, height=card_size, corner_radius=15)
        self.readers_card.pack(side="left", padx=10)
        self.readers_card.pack_propagate(False)
        CTkLabel(
            self.readers_card,
            text=f"Readers\n{summary.get('total_readers', 0)}",
            font=("Arial", 16),
            justify="center"
        ).pack(expand=True)

        # Active Loans Card
        self.loans_card = CTkFrame(self.stats_container, width=card_size, height=card_size, corner_radius=15)
        self.loans_card.pack(side="left", padx=10)
        self.loans_card.pack_propagate(False)
        CTkLabel(
            self.loans_card,
            text=f"Active Loans\n{summary.get('active_loans', 0)}",
            font=("Arial", 16),
            justify="center"
        ).pack(expand=True)

        # ---------------- Main Action Buttons ----------------
        self.buttons_frame = CTkFrame(self.right_frame, corner_radius=15)
        self.buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        CTkLabel(
            self.buttons_frame,
            text="⚡ Quick Actions:",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        btn_w = 350
        btn_h = 65

        CTkButton(
            self.buttons_frame,
            text="📚 Manage Books",
            font=("Arial", 18, "bold"),
            width=btn_w,
            height=btn_h,
            command=self.manage_books
        ).pack(pady=15)

        CTkButton(
            self.buttons_frame,
            text="👥 Manage Readers",
            font=("Arial", 18, "bold"),
            width=btn_w,
            height=btn_h,
            command=self.manage_readers
        ).pack(pady=15)

        CTkButton(
            self.buttons_frame,
            text="🧾 View Loan Records",
            font=("Arial", 18, "bold"),
            width=btn_w,
            height=btn_h,
            command=self.loan_records
        ).pack(pady=15)

        # CTkButton(
        #     self.buttons_frame,
        #     text="📦 Request New Books",
        #     font=("Arial", 18, "bold"),
        #     width=btn_w,
        #     height=btn_h,
        #     command=self.request_books
        # ).pack(pady=15)

        self.root.mainloop()

    # ============================================================
    # Navigation Functions
    # ============================================================
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
