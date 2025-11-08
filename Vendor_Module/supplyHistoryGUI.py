# Vendor_Module/supplyHistoryGUI.py
from customtkinter import *
from tkinter import messagebox
from Vendor_Module.vendorFunctionality import get_all_batches, get_batch_items

set_appearance_mode("dark")

class SupplyHistoryGUI:
    def __init__(self):
        self.root = CTk()
        self.root.title("📊 Supply History")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)

        # ---------------- Title ----------------
        CTkLabel(self.root, text="📊 Supply History", font=("Arial", 22, "bold")).pack(pady=15)

        # ---------------- Filter + Buttons ----------------
        top_frame = CTkFrame(self.root)
        top_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.filter_var = StringVar(value="All")
        filter_menu = CTkOptionMenu(
            top_frame,
            variable=self.filter_var,
            values=["All", "Pending", "Approved", "Rejected"],
            width=200,
            command=self.filter_history
        )
        filter_menu.pack(side="left", padx=10)

        CTkButton(top_frame, text="🔄 Refresh", width=120, command=self.refresh_history).pack(side="left", padx=6)
        CTkButton(top_frame, text="⬅ Back", width=120, command=self.go_back).pack(side="right", padx=10)

        # ---------------- Scrollable Frame ----------------
        self.scroll_frame = CTkScrollableFrame(self.root, width=950, height=450, corner_radius=15)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # ---------------- Data ----------------
        self.selected_batch = None
        self.batches = []
        self.refresh_history()

        self.root.mainloop()

    # ---------------- Load All Batches ----------------
    def refresh_history(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.batches = get_all_batches(self.filter_var.get())

        if not self.batches:
            CTkLabel(self.scroll_frame, text="No supply records found.", font=("Arial", 16, "italic")).pack(pady=20)
            return

        for batch in self.batches:
            text = (
                f"📦 Batch #{batch['batch_id']} | Vendor: {batch['vendor_name']}\n"
                f"Date: {batch['delivery_date']} | Status: {batch['status']} | Total: ₹{batch['total_cost']:.2f}"
            )
            btn = CTkButton(
                self.scroll_frame,
                text=text,
                width=900,
                height=70,
                anchor="w",
                font=("Arial", 14),
                command=lambda b=batch: self.view_details(b)
            )
            btn.pack(pady=6, padx=10)

    # ---------------- Filter ----------------
    def filter_history(self, *args):
        self.refresh_history()

    # ---------------- View Details Popup ----------------
    def view_details(self, batch):
        items = get_batch_items(batch["batch_id"])
        popup = CTkToplevel(self.root)
        popup.title(f"Batch #{batch['batch_id']} Details")
        popup.geometry("650x500")
        popup.resizable(False, False)
        popup.grab_set()
        popup.focus_force()

        CTkLabel(popup, text=f"Vendor: {batch['vendor_name']}", font=("Arial", 18, "bold")).pack(pady=10)
        CTkLabel(popup, text=f"Status: {batch['status']} | Total Cost: ₹{batch['total_cost']:.2f}", font=("Arial", 14)).pack(pady=5)
        if batch.get("admin_remark"):
            CTkLabel(popup, text=f"Remark: {batch['admin_remark']}", font=("Arial", 13, "italic")).pack(pady=5)

        scroll = CTkScrollableFrame(popup, width=600, height=330)
        scroll.pack(padx=10, pady=10)

        if not items:
            CTkLabel(scroll, text="No items recorded in this batch.", font=("Arial", 14, "italic")).pack(pady=20)
            return

        for item in items:
            text = (
                f"📘 {item['title']} by {item['author']}\n"
                f"Qty: {item['quantity']} | Cost: ₹{item['cost_price']:.2f}"
            )
            CTkLabel(scroll, text=text, font=("Arial", 14), anchor="w", justify="left").pack(fill="x", pady=4)

    # ---------------- Back ----------------
    def go_back(self):
        from Admin_Module.adminGUI import AdminGUI  # or Librarian_Module if used there
        self.root.destroy()
        AdminGUI()
