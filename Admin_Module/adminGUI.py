from customtkinter import *
from tkinter import messagebox
from Admin_Module.adminFunctionality import get_admin_stats

set_appearance_mode("dark")

class AdminGUI:
    def __init__(self, u_Id=None, admin_name="Admin"):
        """
        u_Id is optional — you can pass the admin ID if needed.
        admin_name is shown in the welcome label.
        """
        self.u_Id = u_Id
        self.admin_name = admin_name
        self.stats = get_admin_stats()

        # ---------------- Main window ----------------
        self.root = CTk()
        self.root.title("Admin Dashboard")
        self.root.geometry("950x600")
        self.root.resizable(0, 0)

        # ---------------- Main container ----------------
        self.main_frame = CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------------- Left column ----------------
        self.left_frame = CTkFrame(self.main_frame, width=250, corner_radius=15)
        self.left_frame.pack(side="left", fill="y", padx=(10, 5), pady=10)

        # --- Welcome section ---
        self.welcome_frame = CTkFrame(self.left_frame, width=250, corner_radius=15)
        self.welcome_frame.pack(fill="both", padx=10, pady=10)

        # Admin emoji
        self.admin_logo = CTkLabel(
            self.welcome_frame,
            text="🛠",
            font=("Arial", 100)
        )
        self.admin_logo.pack(pady=(20, 10))

        # Centered welcome text (matches ReaderGUI)
        self.welcome_label = CTkLabel(
            self.welcome_frame,
            text=f"Welcome,\n{self.admin_name}",
            font=("Arial", 18, "bold"),
            justify="center",
            anchor="center"
        )
        self.welcome_label.pack(pady=(0, 10), padx=20)

        # --- Info section ---
        self.note_frame = CTkFrame(self.left_frame, width=250, corner_radius=15)
        self.note_frame.pack(fill="both", padx=10, pady=(0, 10))

        self.note_title = CTkLabel(
            self.note_frame,
            text="Admin Panel",
            font=("Arial", 16, "bold"),
            justify="center"
        )
        self.note_title.pack(pady=(10, 5))

        self.note_text = CTkLabel(
            self.note_frame,
            text="Manage users, librarians,\nand books using the options on the right.",
            font=("Arial", 13),
            justify="center",
            wraplength=220
        )
        self.note_text.pack(pady=(0, 12), padx=10)

        # --- Logout button ---
        self.logout_button = CTkButton(
            self.left_frame,
            text="⬅️ Logout",
            font=("Arial", 18, "bold"),
            width=150,
            height=40,
            corner_radius=15,
            command=lambda: self.logout(self.root)
        )
        self.logout_button.pack(pady=10, padx=20, fill="x")

        # ---------------- Right area ----------------
        self.right_frame = CTkFrame(self.main_frame, corner_radius=15)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

        # -------- Stats frames at top --------
        self.stats_frame = CTkFrame(self.right_frame, corner_radius=15)
        self.stats_frame.pack(pady=(10, 20))

        card_size = 150
        self.stats_container = CTkFrame(self.stats_frame, corner_radius=0)
        self.stats_container.pack()

        # --- Card 1: Overall Books Borrowed ---
        self.books_borrowed_card = CTkFrame(self.stats_container, width=card_size, height=card_size, corner_radius=15)
        self.books_borrowed_card.pack(side="left", padx=10)
        self.books_borrowed_card.pack_propagate(False)
        self.books_borrowed_label = CTkLabel(
            self.books_borrowed_card,
            text=f"Books Borrowed:\n{self.stats.get('overall_books_borrowed', 0)}",
            font=("Arial", 16),
            justify="center",
            anchor="center"
        )
        self.books_borrowed_label.pack(expand=True, padx=10, pady=10)

        # --- Card 2: Total Fines (Profit) ---
        self.fines_card = CTkFrame(self.stats_container, width=card_size, height=card_size, corner_radius=15)
        self.fines_card.pack(side="left", padx=10)
        self.fines_card.pack_propagate(False)
        self.fines_label = CTkLabel(
            self.fines_card,
            text=f"Total Fines (₹):\n{self.stats.get('overall_total_fines', 0.0):.2f}",
            font=("Arial", 16),
            justify="center",
            anchor="center"
        )
        self.fines_label.pack(expand=True, padx=10, pady=10)

        # --- Card 3: Active Loans ---
        self.active_loans_card = CTkFrame(self.stats_container, width=card_size, height=card_size, corner_radius=15)
        self.active_loans_card.pack(side="left", padx=10)
        self.active_loans_card.pack_propagate(False)
        self.active_loans_label = CTkLabel(
            self.active_loans_card,
            text=f"Active Loans:\n{self.stats.get('overall_active_loans', 0)}",
            font=("Arial", 16),
            justify="center",
            anchor="center"
        )
        self.active_loans_label.pack(expand=True, padx=10, pady=10)

        # -------- Buttons frame (actions) --------
        self.buttons_frame = CTkFrame(self.right_frame, corner_radius=15)
        self.buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        btn_width = 300
        btn_height = 60

        self.action_label = CTkLabel(
            self.buttons_frame,
            text="⚡ Quick Actions:",
            font=("Arial", 18, "bold"),
            justify="center",
            anchor="center"
        )
        self.action_label.pack(side="top", padx=10, pady=10)

        # --- Buttons ---
        self.manage_users_btn = CTkButton(
            self.buttons_frame,
            text="👥 Manage Users",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=self.open_manage_users
        )
        self.manage_users_btn.pack(pady=20)

        self.register_librarian_btn = CTkButton(
            self.buttons_frame,
            text="➕ Register New Librarian",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=self.open_register_librarian
        )
        self.register_librarian_btn.pack(pady=20)

        self.manage_books_btn = CTkButton(
            self.buttons_frame,
            text="📚 Manage Books",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=self.open_manage_books
        )
        self.manage_books_btn.pack(pady=20)

        # --- Footer ---
        self.footer_frame = CTkFrame(self.right_frame)
        self.footer_frame.pack(fill="x", padx=10, pady=(0, 8))
        CTkButton(self.footer_frame, text="Refresh Stats", width=140, command=self.refresh_stats).pack(side="left", padx=(0, 8))
        CTkButton(self.footer_frame, text="Close", width=140, command=self.root.destroy).pack(side="right", padx=(8, 0))

        self.root.mainloop()

    # ---------------- Action handlers ----------------
    def refresh_stats(self):
        self.stats = get_admin_stats()
        self.books_borrowed_label.configure(text=f"Books Borrowed:\n{self.stats.get('overall_books_borrowed', 0)}")
        self.fines_label.configure(text=f"Total Fines (₹):\n{self.stats.get('overall_total_fines', 0.0):.2f}")
        self.active_loans_label.configure(text=f"Active Loans:\n{self.stats.get('overall_active_loans', 0)}")

    def open_manage_users(self):
        try:
            from Admin_Module.manageUsersGUI import ManageUsersGUI
            self.root.destroy()
            ManageUsersGUI(self.u_Id)
        except Exception as e:
            messagebox.showinfo("Manage Users", f"Manage Users GUI not implemented yet.\n{e}")

    def open_register_librarian(self):
        try:
            from Admin_Module.registerLibrarianGUI import RegisterLibrarianGUI
            self.root.destroy()
            RegisterLibrarianGUI(self.u_Id)
        except Exception as e:
            messagebox.showinfo("Register Librarian", f"Register Librarian GUI not implemented yet.\n{e}")

    def open_manage_books(self):
        try:
            from Admin_Module.manageBooksGUI import ManageBooksGUI
            self.root.destroy()
            ManageBooksGUI(self.u_Id)
        except Exception as e:
            messagebox.showinfo("Manage Books", f"Manage Books GUI not implemented yet.\n{e}")

    def logout(self, window):
        try:
            from Login_Module.loginGUI import LoginGUI
            window.destroy()
            root = CTk()
            app = LoginGUI(root)
            root.mainloop()
        except Exception as e:
            messagebox.showerror("Logout Error", f"Could not logout: {e}")
