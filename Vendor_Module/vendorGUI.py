# Vendor_Module/vendorGUI.py
from customtkinter import *
from tkinter import messagebox

from Vendor_Module.vendorFunctionality import (
    get_vendor_requests,
    update_request_status,
    mark_request_supplied,
    get_vendor_details,   # <-- imported
)
from Vendor_Module.supplyHistoryGUI import SupplyHistoryGUI

set_appearance_mode("dark")


class VendorGUI:
    def __init__(self, u_Id, vendor_id):
        self.u_Id = u_Id
        self.vendor_id = vendor_id

        # ===== NEW: Fetch Vendor Name =====
        vendor_data = get_vendor_details(vendor_id)
        self.vendor_name = vendor_data["company"] if vendor_data and "company" in vendor_data else "Vendor"

        # ---------------- Main Window ----------------
        self.root = CTk()
        self.root.title("Vendor Dashboard")
        self.root.geometry("1050x650")
        self.root.resizable(0, 0)

        # ---------------- Main container ----------------
        self.main_frame = CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ============================================================
        # LEFT SIDEBAR (Same layout style as Reader Dashboard)
        # ============================================================
        self.left_frame = CTkFrame(self.main_frame, width=250, corner_radius=15)
        self.left_frame.pack(side="left", fill="y", padx=(10, 5), pady=10)

        # ---------------- Vendor Icon & Welcome -------------------
        self.welcome_frame = CTkFrame(self.left_frame, corner_radius=15)
        self.welcome_frame.pack(fill="x", padx=10, pady=10)

        self.vendor_icon = CTkLabel(self.welcome_frame, text="🏬", font=("Arial", 100))
        self.vendor_icon.pack(pady=(20, 10))

        self.vendor_label = CTkLabel(
            self.welcome_frame,
            text=f"{self.vendor_name}",
            font=("Arial", 18, "bold"),
            justify="center"
        )
        self.vendor_label.pack(pady=(0, 20))

        # ---------------- Buttons in Left Sidebar ----------------
        self.history_btn = CTkButton(
            self.left_frame,
            text="📦 Supply History",
            font=("Arial", 18, "bold"),
            width=180,
            height=40,
            corner_radius=15,
            command=self.open_supply_history  # method exists now
        )
        self.history_btn.pack(pady=20, padx=20, fill="x")

        self.logout_btn = CTkButton(
            self.left_frame,
            text="⬅ Logout",
            font=("Arial", 18, "bold"),
            width=180,
            height=40,
            corner_radius=15,
            fg_color="#c0392b",
            command=self.logout  # normalized to no-arg
        )
        self.logout_btn.pack(pady=20, padx=20, fill="x")

        # ============================================================
        # RIGHT SIDE CONTENT AREA = Stats + Quick Actions + Requests
        # ============================================================
        self.right_frame = CTkFrame(self.main_frame, corner_radius=15)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

        # ---------------- Stats Section ----------------
        self.stats_frame = CTkFrame(self.right_frame, corner_radius=15)
        self.stats_frame.pack(pady=(10, 20))

        card_size = 150
        self.stats_container = CTkFrame(self.stats_frame)
        self.stats_container.pack()

        # Total Requests Card
        self.total_req_card = CTkFrame(self.stats_container, width=card_size, height=card_size, corner_radius=15)
        self.total_req_card.pack(side="left", padx=10)
        self.total_req_card.pack_propagate(False)
        CTkLabel(self.total_req_card, text="Total Requests\n—", font=("Arial", 16)).pack(expand=True)

        # Pending Requests Card
        self.pending_req_card = CTkFrame(self.stats_container, width=card_size, height=card_size, corner_radius=15)
        self.pending_req_card.pack(side="left", padx=10)
        self.pending_req_card.pack_propagate(False)
        CTkLabel(self.pending_req_card, text="Pending Requests\n—", font=("Arial", 16)).pack(expand=True)

        # Supplied Requests Card
        self.supplied_req_card = CTkFrame(self.stats_container, width=card_size, height=card_size, corner_radius=15)
        self.supplied_req_card.pack(side="left", padx=10)
        self.supplied_req_card.pack_propagate(False)
        CTkLabel(self.supplied_req_card, text="Supplied Requests\n—", font=("Arial", 16)).pack(expand=True)

        # ---------------- Incoming Requests List ----------------
        self.requests_label = CTkLabel(
            self.right_frame,
            text="📨 Incoming Requests:",
            font=("Arial", 18, "bold")
        )
        self.requests_label.pack(pady=(10, 5))

        self.scroll_frame = CTkScrollableFrame(self.right_frame, width=900, height=300, corner_radius=15)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Load Requests
        self.load_requests()

        self.root.mainloop()

    # ---------------- Open Supply History ----------------
    def open_supply_history(self):
        self.root.withdraw()   # hide vendor window
        SupplyHistoryGUI(self.u_Id, self.vendor_id, parent=self.root)

    # ---------------- Load Requests ----------------
    def load_requests(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        requests = get_vendor_requests(self.vendor_id) or []

        # Update stats cards
        total = len(requests)
        pending = sum(1 for r in requests if r.get("status") == "Pending")
        supplied = sum(1 for r in requests if r.get("status") == "Supplied")

        # Update labels safely (first child is label)
        try:
            self.total_req_card.winfo_children()[0].configure(text=f"Total Requests\n{total}")
            self.pending_req_card.winfo_children()[0].configure(text=f"Pending Requests\n{pending}")
            self.supplied_req_card.winfo_children()[0].configure(text=f"Supplied\n{supplied}")
        except Exception:
            pass

        if not requests:
            CTkLabel(self.scroll_frame, text="No requests found.", font=("Arial", 14, "italic")).pack(pady=20)
            return

        for r in requests:
            card = CTkFrame(self.scroll_frame, corner_radius=12)
            card.pack(fill="x", padx=10, pady=10)

            info = (
                f"📘 {r.get('book_title','-')} by {r.get('author') or 'Unknown'}\n"
                f"🔢 Qty: {r.get('quantity','-')} | 📅 {r.get('request_date','-')}\n"
                f"👤 {r.get('librarian_name','-')} ({r.get('librarian_email','-')})\n"
                f"📌 Status: {r.get('status','-')}"
            )

            CTkLabel(card, text=info, justify="left", font=("Arial", 15), anchor="w").pack(
                side="left", padx=10, pady=10
            )

            btn_frame = CTkFrame(card, fg_color="transparent")
            btn_frame.pack(side="right", padx=10, pady=10)

            status = r.get("status", "")
            rid = r.get("request_id")
            if status == "Pending":
                CTkButton(btn_frame, text="✅ Approve", width=120,
                          command=lambda rid=rid: self.change_status(rid, "Approved")).pack(pady=5)
                CTkButton(btn_frame, text="❌ Reject", width=120, fg_color="#c0392b",
                          command=lambda rid=rid: self.change_status(rid, "Rejected")
                          ).pack(pady=5)
            elif status == "Approved":
                CTkButton(btn_frame, text="📦 Mark Supplied", width=140, fg_color="#2980b9",
                          command=lambda rid=rid: self.mark_supplied(rid)
                          ).pack(pady=10)

    # ---------------- Change Status ----------------
    def change_status(self, request_id, new_status):
        if not request_id:
            messagebox.showerror("Error", "Request id missing.")
            return
        if messagebox.askyesno("Confirm", f"Mark this request as {new_status}?"):
            try:
                if update_request_status(request_id, new_status):
                    messagebox.showinfo("Success", f"Request marked as {new_status}.")
                    self.load_requests()
                else:
                    messagebox.showerror("Error", "Failed to update request.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update request: {e}")

    # ---------------- Mark Supplied ----------------
    def mark_supplied(self, request_id):
        if not request_id:
            messagebox.showerror("Error", "Request id missing.")
            return
        if messagebox.askyesno("Confirm", "Mark this request as Supplied?"):
            try:
                if mark_request_supplied(request_id):
                    messagebox.showinfo("Success", "Marked as Supplied.")
                    self.load_requests()
                else:
                    messagebox.showerror("Error", "Marked as Supplied failed.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to mark supplied: {e}")

    # ---------------- Logout ----------------
    def logout(self):
        try:
            self.root.destroy()
        except Exception:
            pass
        from Login_Module.loginGUI import LoginGUI
        root = CTk()
        LoginGUI(root)
        root.mainloop()
