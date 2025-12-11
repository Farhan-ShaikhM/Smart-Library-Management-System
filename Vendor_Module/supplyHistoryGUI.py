# Vendor_Module/supplyHistoryGUI.py
from customtkinter import *
from tkinter import messagebox
from Vendor_Module.supplyHistoryFunctionality import get_supplied_requests

set_appearance_mode("dark")


class SupplyHistoryGUI:
    def __init__(self, u_Id, vendor_id, parent=None):
        self.u_Id = u_Id
        self.vendor_id = vendor_id
        self.parent = parent

        self.root = CTk()
        self.root.title("📦 Supply History")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)

        # =========================================================
        # HEADER
        # =========================================================
        header = CTkFrame(self.root, fg_color="#1e1e1e", height=70, corner_radius=0)
        header.pack(fill="x")

        CTkLabel(
            header,
            text="📦 Supply History",
            font=("Arial", 26, "bold")
        ).pack(side="left", padx=20)

        CTkButton(
            header,
            text="⬅ Back",
            width=120,
            height=35,
            corner_radius=15,
            fg_color="#34495e",
            hover_color="#2c3e50",
            command=self.go_back
        ).pack(side="right", padx=20)

        # =========================================================
        # MAIN AREA
        # =========================================================
        main_frame = CTkFrame(self.root, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        CTkLabel(
            main_frame,
            text="All Supplied Requests",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))

        # Scrollable list
        self.scroll_frame = CTkScrollableFrame(main_frame, width=920, height=500, corner_radius=15)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_supplies()
        self.root.mainloop()

    # =========================================================
    # LOAD SUPPLY RECORDS
    # =========================================================
    def load_supplies(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        supplies = get_supplied_requests(self.vendor_id)

        if not supplies:
            CTkLabel(
                self.scroll_frame,
                text="No supplied requests found.",
                font=("Arial", 15, "italic")
            ).pack(pady=30)
            return

        # Create a stylish card for each item
        for s in supplies:
            frame = CTkFrame(self.scroll_frame, corner_radius=15, fg_color="#2c2c2c")
            frame.pack(fill="x", pady=10, padx=10)

            # Card Content
            CTkLabel(
                frame,
                text=f"📘 {s['book_title']}  —  {s['author'] or 'Unknown'}",
                font=("Arial", 17, "bold"),
                anchor="w"
            ).pack(anchor="w", padx=15, pady=(10, 2))

            CTkLabel(
                frame,
                text=f"🔢 Quantity: {s['quantity']}    |    📅 Supplied On: {s['supply_date']}",
                font=("Arial", 14),
                anchor="w"
            ).pack(anchor="w", padx=15)

            CTkLabel(
                frame,
                text=f"👤 Supplied To: {s['librarian_name']} ({s['librarian_email']})",
                font=("Arial", 14),
                anchor="w"
            ).pack(anchor="w", padx=15, pady=(0, 12))

    # =========================================================
    # GO BACK
    # =========================================================
    def go_back(self):
        self.root.destroy()
        if self.parent:
            self.parent.deiconify()
