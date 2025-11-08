# Admin_Module/adminGUI.py
from customtkinter import *
from tkinter import messagebox
from Librarian_Module.librarianFunctionality import get_librarian_dashboard_data

set_appearance_mode("dark")

class AdminGUI:
    def __init__(self):
        self.admin_name = "Admin"  # You can make this dynamic if linked to login
        self.stats = get_librarian_dashboard_data()  # reuse same stats query for now

        # ---------------- Main Window ----------------
        self.root = CTk()
        self.root.title("🏛️ Admin Dashboard")
        self.root.geometry("950x600")
        self.root.resizable(0, 0)

        # ---------------- Main Container ----------------
        self.main_frame = CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------------- Left Sidebar ----------------
        self.left_frame = CTkFrame(self.main_frame, width=250, corner_radius=15)
        self.left_frame.pack(side="left", fill="y", padx=(10, 5), pady=10)

        # Profile Section
        self.profile_frame = CTkFrame(self.left_frame, corner_radius=15)
        self.profile_frame.pack(fill="both", padx=10, pady=(10, 10))

        self.user_logo = CTkLabel(self.profile_frame, text="🧑‍💼", font=("Arial", 100))
        self.user_logo.pack(pady=(20, 10))

        self.welcome_label = CTkLabel(
            self.profile_frame,
            text=f"Welcome,\n{self.admin_name}",
            font=("Arial", 18, "bold"),
            justify="center"
        )
        self.welcome_label.pack(pady=(0, 10), padx=20)

        # Note or Tips Section
        self.note_frame = CTkFrame(self.left_frame, corner_radius=15)
        self.note_frame.pack(fill="both", padx=10, pady=(0, 10))

        CTkLabel(
            self.note_frame,
            text="⚙️ Admin Panel\nManage vendors, librarians, and approvals.",
            font=("Arial", 14),
            justify="center",
            wraplength=200
        ).pack(pady=20, padx=20)

        # Logout Button
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

        # -------- Dashboard Stats (Top Cards) --------
        self.stats_frame = CTkFrame(self.right_frame, corner_radius=15)
        self.stats_frame.pack(pady=(10, 20))

        stats_container = CTkFrame(self.stats_frame, corner_radius=0)
        stats_container.pack()

        self.create_stat_card(stats_container, "📚 Total Books", self.stats.get("total_books", 0)).pack(side="left", padx=10)
        self.create_stat_card(stats_container, "👥 Total Readers", self.stats.get("total_readers", 0)).pack(side="left", padx=10)
        self.create_stat_card(stats_container, "📦 Active Loans", self.stats.get("active_loans", 0)).pack(side="left", padx=10)
        self.create_stat_card(stats_container, "⏰ Overdue Loans", self.stats.get("overdue_loans", 0)).pack(side="left", padx=10)

        # -------- Quick Action Buttons --------
        self.buttons_frame = CTkFrame(self.right_frame, corner_radius=15)
        self.buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        CTkLabel(
            self.buttons_frame,
            text="⚡ Quick Actions:",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        btn_width = 300
        btn_height = 60

        CTkButton(
            self.buttons_frame,
            text="📋 Manage Vendors",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=self.manage_vendors
        ).pack(pady=10)

        CTkButton(
            self.buttons_frame,
            text="📦 Create Supply Batch",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=self.create_supply_batch
        ).pack(pady=10)

        CTkButton(
            self.buttons_frame,
            text="✅ Approve Supply Batches",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=self.approve_batches
        ).pack(pady=10)

        CTkButton(
            self.buttons_frame,
            text="📊 View Supply History",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=self.supply_history
        ).pack(pady=10)

        # Optional Librarian Access
        CTkButton(
            self.buttons_frame,
            text="👩‍🏫 Librarian Dashboard",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=self.open_librarian_dashboard
        ).pack(pady=10)

        self.root.mainloop()

    # ---------------- Helper: Stat Card ----------------
    def create_stat_card(self, parent, title, value):
        frame = CTkFrame(parent, width=150, height=150, corner_radius=15)
        frame.pack_propagate(False)
        CTkLabel(frame, text=title, font=("Arial", 16, "bold")).pack(pady=(10, 0))
        CTkLabel(frame, text=str(value), font=("Arial", 24, "bold"), text_color="#00FFAA").pack(pady=(10, 10))
        return frame

    # ---------------- Navigation Buttons ----------------
    def manage_vendors(self):
        from Vendor_Module.vendorGUI import VendorGUI
        self.root.destroy()
        VendorGUI()

    def create_supply_batch(self):
        from Vendor_Module.supplyBatchGUI import SupplyBatchGUI
        self.root.destroy()
        SupplyBatchGUI(opened_by="Admin")

    def approve_batches(self):
        from Vendor_Module.batchApprovalGUI import BatchApprovalGUI
        self.root.destroy()
        BatchApprovalGUI()

    def supply_history(self):
        from Vendor_Module.supplyHistoryGUI import SupplyHistoryGUI
        self.root.destroy()
        SupplyHistoryGUI()

    def open_librarian_dashboard(self):
        from Librarian_Module.librarianGUI import LibrarianGUI
        self.root.destroy()
        LibrarianGUI()

    def logout(self):
        from Login_Module.loginGUI import LoginGUI
        self.root.destroy()
        messagebox.showinfo("Logout", "You have been logged out successfully.")
        root = CTk()
        LoginGUI(root)
        root.mainloop()
