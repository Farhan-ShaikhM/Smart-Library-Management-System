# Vendor_Module/batchApprovalGUI.py
from customtkinter import *
from tkinter import messagebox
from Vendor_Module.vendorFunctionality import (
    get_all_batches,
    get_batch_items,
    approve_batch,
    reject_batch
)

set_appearance_mode("dark")

class BatchApprovalGUI:
    def __init__(self):
        self.root = CTk()
        self.root.title("📋 Supply Batch Approval")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)

        # ---------------- Title ----------------
        CTkLabel(self.root, text="📦 Supply Batch Approval", font=("Arial", 22, "bold")).pack(pady=15)

        # ---------------- Filter & Buttons ----------------
        top_frame = CTkFrame(self.root)
        top_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.filter_var = StringVar(value="Pending")
        filter_menu = CTkOptionMenu(
            top_frame,
            variable=self.filter_var,
            values=["Pending", "Approved", "Rejected", "All"],
            width=200,
            command=self.filter_batches
        )
        filter_menu.pack(side="left", padx=10)

        CTkButton(top_frame, text="🔄 Refresh", width=120, command=self.refresh_batches).pack(side="left", padx=6)
        CTkButton(top_frame, text="⬅ Back", width=120, command=self.go_back).pack(side="right", padx=10)

        # ---------------- Scrollable Batch List ----------------
        self.scroll_frame = CTkScrollableFrame(self.root, width=950, height=400, corner_radius=15)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # ---------------- Action Buttons ----------------
        action_frame = CTkFrame(self.root)
        action_frame.pack(pady=10)
        CTkButton(action_frame, text="✅ Approve Batch", width=180, command=self.approve_selected).grid(row=0, column=0, padx=10)
        CTkButton(action_frame, text="❌ Reject Batch", width=180, command=self.reject_selected).grid(row=0, column=1, padx=10)
        CTkButton(action_frame, text="🔍 View Batch Details", width=180, command=self.view_details).grid(row=0, column=2, padx=10)

        # ---------------- Data ----------------
        self.selected_batch = None
        self.batches = []
        self.refresh_batches()

        self.root.mainloop()

    # ---------------- Load Batches ----------------
    def refresh_batches(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.batches = get_all_batches(self.filter_var.get())

        if not self.batches:
            CTkLabel(self.scroll_frame, text="No batches found.", font=("Arial", 16, "italic")).pack(pady=20)
            return

        for batch in self.batches:
            text = (
                f"📦 Batch #{batch['batch_id']} | Vendor: {batch['vendor_name']}\n"
                f"Date: {batch['delivery_date']} | Status: {batch['status']} | Total Cost: ₹{batch['total_cost']:.2f}"
            )
            btn = CTkButton(
                self.scroll_frame,
                text=text,
                width=900,
                height=70,
                anchor="w",
                font=("Arial", 14),
                command=lambda b=batch: self.select_batch(b)
            )
            btn.pack(pady=6, padx=10)

    # ---------------- Select Batch ----------------
    def select_batch(self, batch):
        self.selected_batch = batch
        messagebox.showinfo("Batch Selected", f"Selected Batch ID: {batch['batch_id']}\nVendor: {batch['vendor_name']}")

    # ---------------- View Batch Details ----------------
    def view_details(self):
        if not self.selected_batch:
            messagebox.showwarning("Warning", "Please select a batch first.")
            return

        items = get_batch_items(self.selected_batch["batch_id"])
        if not items:
            messagebox.showinfo("Info", "No items found in this batch.")
            return

        popup = CTkToplevel(self.root)
        popup.title(f"Batch #{self.selected_batch['batch_id']} Details")
        popup.geometry("650x450")
        popup.resizable(False, False)
        popup.grab_set()
        popup.focus_force()

        CTkLabel(popup, text=f"Vendor: {self.selected_batch['vendor_name']}", font=("Arial", 18, "bold")).pack(pady=10)
        CTkLabel(popup, text=f"Status: {self.selected_batch['status']}", font=("Arial", 14)).pack(pady=5)

        scroll = CTkScrollableFrame(popup, width=600, height=300)
        scroll.pack(padx=10, pady=10)

        for item in items:
            text = (
                f"📘 {item['title']} by {item['author']}\n"
                f"Qty: {item['quantity']} | Cost: ₹{item['cost_price']:.2f}"
            )
            CTkLabel(scroll, text=text, font=("Arial", 14), justify="left", anchor="w").pack(fill="x", pady=4)

    # ---------------- Approve Batch ----------------
    def approve_selected(self):
        if not self.selected_batch:
            messagebox.showwarning("Warning", "Select a batch first.")
            return
        if self.selected_batch["status"] != "Pending":
            messagebox.showinfo("Info", "Only pending batches can be approved.")
            return

        popup = CTkToplevel(self.root)
        popup.title("Approve Batch")
        popup.geometry("400x250")
        popup.grab_set()
        popup.focus_force()

        CTkLabel(popup, text=f"Batch #{self.selected_batch['batch_id']}", font=("Arial", 18, "bold")).pack(pady=10)
        CTkLabel(popup, text="Enter Remark (optional):", font=("Arial", 14)).pack(pady=5)
        remark_entry = CTkTextbox(popup, width=300, height=80)
        remark_entry.pack(pady=5)

        def approve_action():
            remark = remark_entry.get("1.0", "end").strip()
            success = approve_batch(self.selected_batch["batch_id"], remark)
            if success:
                messagebox.showinfo("Success", "Batch approved successfully! ✅\nBook stock updated.")
                popup.destroy()
                self.refresh_batches()
            else:
                messagebox.showerror("Error", "Failed to approve batch.")

        CTkButton(popup, text="Approve", width=150, command=approve_action).pack(pady=10)

    # ---------------- Reject Batch ----------------
    def reject_selected(self):
        if not self.selected_batch:
            messagebox.showwarning("Warning", "Select a batch first.")
            return
        if self.selected_batch["status"] != "Pending":
            messagebox.showinfo("Info", "Only pending batches can be rejected.")
            return

        popup = CTkToplevel(self.root)
        popup.title("Reject Batch")
        popup.geometry("400x250")
        popup.grab_set()
        popup.focus_force()

        CTkLabel(popup, text=f"Batch #{self.selected_batch['batch_id']}", font=("Arial", 18, "bold")).pack(pady=10)
        CTkLabel(popup, text="Enter Remark (required):", font=("Arial", 14)).pack(pady=5)
        remark_entry = CTkTextbox(popup, width=300, height=80)
        remark_entry.pack(pady=5)

        def reject_action():
            remark = remark_entry.get("1.0", "end").strip()
            if not remark:
                messagebox.showerror("Error", "Remark is required when rejecting a batch.")
                return

            success = reject_batch(self.selected_batch["batch_id"], remark)
            if success:
                messagebox.showinfo("Success", "Batch rejected successfully. ❌")
                popup.destroy()
                self.refresh_batches()
            else:
                messagebox.showerror("Error", "Failed to reject batch.")

        CTkButton(popup, text="Reject", width=150, command=reject_action).pack(pady=10)

    # ---------------- Filter ----------------
    def filter_batches(self, *args):
        self.refresh_batches()

    # ---------------- Back ----------------
    def go_back(self):
        from Admin_Module.adminGUI import AdminGUI
        self.root.destroy()
        AdminGUI()
