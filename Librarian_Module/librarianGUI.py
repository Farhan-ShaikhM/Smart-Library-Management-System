# Librarian_Module/librarianGUI.py
from customtkinter import *
from tkinter import messagebox
from Librarian_Module.librarianFunctionality import get_librarian_dashboard_data

set_appearance_mode("dark")

class LibrarianGUI:
    def __init__(self):
        self.librarian_name = "Librarian"  # ✅ Changed from 'Admin Librarian' to 'Librarian'
        self.stats = get_librarian_dashboard_data()

        # ---------------- Main Window ----------------
        self.root = CTk()
        self.root.title("📘 Librarian Dashboard")  # ✅ Updated window title
        self.root.geometry("950x600")
        self.root.resizable(0, 0)

        # ---------------- Main container ----------------
        self.main_frame = CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------------- Left Sidebar ----------------
        self.left_frame = CTkFrame(self.main_frame, width=250, corner_radius=15)
        self.left_frame.pack(side="left", fill="y", padx=(10,5), pady=10)

        self.welcome_frame = CTkFrame(self.left_frame, width=250, corner_radius=15)
        self.welcome_frame.pack(fill="both", padx=10, pady=10)

        # Librarian emoji
        self.user_logo = CTkLabel(self.welcome_frame, text="👩‍🏫", font=("Arial", 100))
        self.user_logo.pack(pady=(20, 10))

        # Welcome label
        self.welcome_label = CTkLabel(
            self.welcome_frame,
            text=f"Welcome,\n{self.librarian_name}",
            font=("Arial", 18, "bold"),
            justify="center"
        )
        self.welcome_label.pack(pady=(0, 10), padx=20)

        # Note frame
        self.note_frame = CTkFrame(self.left_frame, width=250, corner_radius=15)
        self.note_frame.pack(fill="both", padx=10, pady=(0,10))

        CTkLabel(
            self.note_frame,
            text="📖 Librarian Panel\nManage Books, Readers & Loans.",
            font=("Arial", 14),
            justify="center",
            wraplength=200
        ).pack(pady=20, padx=20)

        # Logout button
        self.logout_button = CTkButton(
            self.left_frame,
            text="⬅️ Logout",
            font=("Arial", 18, "bold"),
            width=150,
            height=40,
            corner_radius=15,
            command=self.logout
        )
        self.logout_button.pack(pady=20, padx=20, fill="x")

        # ---------------- Right Section ----------------
        self.right_frame = CTkFrame(self.main_frame, corner_radius=15)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

        # -------- Stats frames at top --------
        self.stats_frame = CTkFrame(self.right_frame, corner_radius=15)
        self.stats_frame.pack(pady=(10, 20))

        stats_container = CTkFrame(self.stats_frame, corner_radius=0)
        stats_container.pack()

        # Statistic cards
        self.create_stat_card(stats_container, "📚 Total Books", self.stats.get("total_books", 0)).pack(side="left", padx=10)
        self.create_stat_card(stats_container, "👥 Total Readers", self.stats.get("total_readers", 0)).pack(side="left", padx=10)
        self.create_stat_card(stats_container, "📦 Active Loans", self.stats.get("active_loans", 0)).pack(side="left", padx=10)
        self.create_stat_card(stats_container, "⏰ Overdue Loans", self.stats.get("overdue_loans", 0)).pack(side="left", padx=10)

        # -------- Quick Actions Section --------
        self.buttons_frame = CTkFrame(self.right_frame, corner_radius=15)
        self.buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.action_label = CTkLabel(
            self.buttons_frame,
            text="⚡ Quick Actions",
            font=("Arial", 18, "bold")
        )
        self.action_label.pack(side="top", padx=10, pady=10)

        btn_width = 300
        btn_height = 60

        CTkButton(
            self.buttons_frame,
            text="📗 Manage Books",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=self.manage_books
        ).pack(pady=20)

        CTkButton(
            self.buttons_frame,
            text="👥 Manage Readers",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=self.manage_readers
        ).pack(pady=20)

        CTkButton(
            self.buttons_frame,
            text="🧾 Loan Records",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=self.loan_records
        ).pack(pady=20)

        self.root.mainloop()

    # ---------------- Helper to create stat cards ----------------
    def create_stat_card(self, parent, title, value):
        frame = CTkFrame(parent, width=150, height=150, corner_radius=15)
        frame.pack_propagate(False)
        CTkLabel(frame, text=title, font=("Arial", 16, "bold")).pack(pady=(10, 0))
        CTkLabel(frame, text=str(value), font=("Arial", 24, "bold"), text_color="#00FFAA").pack(pady=(10, 10))
        return frame

    # ---------------- Navigation Buttons ----------------
    def manage_books(self):
        from Librarian_Module.manageBooksGUI import ManageBooksGUI
        self.root.destroy()
        ManageBooksGUI()

    def manage_readers(self):
        from Librarian_Module.manageReadersGUI import ManageReadersGUI
        self.root.destroy()
        ManageReadersGUI()

    def loan_records(self):
        from Librarian_Module.loanRecordsGUI import LoanRecordsGUI
        self.root.destroy()
        LoanRecordsGUI()

    # ---------------- Logout ----------------
    def logout(self):
        from Login_Module.loginGUI import LoginGUI
        self.root.destroy()
        messagebox.showinfo("Logout", "You have been logged out successfully.")
        root = CTk()
        LoginGUI(root)
        root.mainloop()
