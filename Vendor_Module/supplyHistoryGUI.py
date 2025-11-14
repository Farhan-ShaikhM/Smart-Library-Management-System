# Vendor_Module/supplyHistoryGUI.py
from customtkinter import *
from tkinter import messagebox
from Vendor_Module.supplyHistoryFunctionality import get_supplied_requests

set_appearance_mode("dark")


class SupplyHistoryGUI:
    def __init__(self, u_Id, vendor_id):
        self.u_Id = u_Id
        self.vendor_id = vendor_id
        self.root = CTk()
        self.root.title("📦 Supply History")
        self.root.geometry("950x650")
        self.root.resizable(False, False)

        # ---------- Header ----------
        CTkLabel(self.root, text="📦 Supply History", font=("Arial", 24, "bold")).pack(pady=20)
        CTkButton(self.root, text="⬅ Back", width=150, command=self.go_back).pack(pady=(0, 15))

        # ---------- Supply List ----------
        self.scroll_frame = CTkScrollableFrame(self.root, width=900, height=500)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.load_supplies()
        self.root.mainloop()

    def load_supplies(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        supplies = get_supplied_requests(self.vendor_id)
        if not supplies:
            CTkLabel(self.scroll_frame, text="No supplied requests found.", font=("Arial", 14, "italic")).pack(pady=20)
            return

        for s in supplies:
            info = (
                f"📘 {s['book_title']} by {s['author'] or 'Unknown'}\n"
                f"Qty: {s['quantity']} | Supplied on: {s['supply_date']}\n"
                f"To: {s['librarian_name']} ({s['librarian_email']})"
            )

            frame = CTkFrame(self.scroll_frame, corner_radius=10)
            frame.pack(fill="x", pady=6, padx=10)

            CTkLabel(frame, text=info, font=("Arial", 14), justify="left", anchor="w").pack(side="left", padx=10)

    def go_back(self):
        from Vendor_Module.vendorGUI import VendorGUI
        self.root.destroy()
        VendorGUI(self.u_Id, self.vendor_id)
