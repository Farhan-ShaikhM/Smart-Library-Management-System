# Vendor_Module/vendorGUI.py
from customtkinter import *
from tkinter import messagebox
from Vendor_Module.vendorFunctionality import (
    get_vendor_requests, update_request_status, mark_request_supplied
)
from Vendor_Module.supplyHistoryGUI import SupplyHistoryGUI  # <-- moved outside & fixed position

set_appearance_mode("dark")


class VendorGUI:
    def __init__(self, u_Id, vendor_id):
        self.u_Id = u_Id
        self.vendor_id = vendor_id
        self.root = CTk()
        self.root.title("🏢 Vendor Dashboard")
        self.root.geometry("950x650")
        self.root.resizable(False, False)

        # ---------- Header ----------
        CTkLabel(self.root, text="🏢 Vendor Dashboard", font=("Arial", 24, "bold")).pack(pady=20)
        CTkButton(self.root, text="⬅ Logout", width=150, command=self.logout).pack(pady=(0, 15))
        CTkButton(self.root, text="📦 View Supply History", width=200,
                  command=self.open_supply_history).pack(pady=10)
        CTkLabel(self.root, text=f"Vendor ID: {self.vendor_id}", font=("Arial", 14)).pack()

        # ---------- Requests ----------
        CTkLabel(self.root, text="📦 Librarian Requests", font=("Arial", 18, "bold")).pack(pady=5)
        self.scroll_frame = CTkScrollableFrame(self.root, width=900, height=500)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.load_requests()
        self.root.mainloop()

    # ---------- Open Supply History ----------
    def open_supply_history(self):
        self.root.destroy()
        SupplyHistoryGUI(self.u_Id, self.vendor_id)

    # ---------- Load Requests ----------
    def load_requests(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        requests = get_vendor_requests(self.vendor_id)
        if not requests:
            CTkLabel(self.scroll_frame, text="No requests found.", font=("Arial", 14, "italic")).pack(pady=20)
            return

        for r in requests:
            info = (f"📘 {r['book_title']} by {r['author'] or 'Unknown'}\n"
                    f"Qty: {r['quantity']} | Requested: {r['request_date']}\n"
                    f"By: {r['librarian_name']} ({r['librarian_email']})\n"
                    f"Status: {r['status']}")

            frame = CTkFrame(self.scroll_frame, corner_radius=10)
            frame.pack(fill="x", pady=6, padx=10)

            CTkLabel(frame, text=info, font=("Arial", 14), justify="left", anchor="w").pack(side="left", padx=10)

            # Buttons for status control
            if r["status"] == "Pending":
                CTkButton(frame, text="✅ Approve", width=120,
                          command=lambda rid=r["request_id"]: self.change_status(rid, "Approved")).pack(side="right", padx=5)
                CTkButton(frame, text="❌ Reject", width=120, fg_color="red",
                          command=lambda rid=r["request_id"]: self.change_status(rid, "Rejected")).pack(side="right", padx=5)
            elif r["status"] == "Approved":
                CTkButton(frame, text="📦 Mark Supplied", width=150,
                          command=lambda rid=r["request_id"]: self.mark_supplied(rid)).pack(side="right", padx=10)

    # ---------- Change Status ----------
    def change_status(self, request_id, new_status):
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to mark this as {new_status}?")
        if not confirm:
            return
        if update_request_status(request_id, new_status):
            messagebox.showinfo("Success", f"Request marked as {new_status}.")
            self.load_requests()
        else:
            messagebox.showerror("Error", "Failed to update request.")

    # ---------- Mark Supplied ----------
    def mark_supplied(self, request_id):
        confirm = messagebox.askyesno("Confirm", "Mark this request as Supplied?")
        if not confirm:
            return
        if mark_request_supplied(request_id):
            messagebox.showinfo("Success", "Marked as Supplied successfully!")
            self.load_requests()
        else:
            messagebox.showerror("Error", "Failed to mark as supplied.")

    # ---------- Logout ----------
    def logout(self):
        from Login_Module.loginGUI import LoginGUI
        self.root.destroy()
        root = CTk()
        LoginGUI(root)
        root.mainloop()
