# Vendor_Module/vendorGUI.py
from customtkinter import *
from tkinter import messagebox
from Vendor_Module.vendorFunctionality import (
    get_all_vendors,
    add_vendor,
    update_vendor,
    delete_vendor
)

set_appearance_mode("dark")

class VendorGUI:
    def __init__(self):
        self.root = CTk()
        self.root.title("📋 Manage Vendors")
        self.root.geometry("950x600")
        self.root.resizable(False, False)

        # ---------------- Title ----------------
        CTkLabel(self.root, text="📦 Vendor Management", font=("Arial", 22, "bold")).pack(pady=15)

        # ---------------- Search Bar ----------------
        top_frame = CTkFrame(self.root)
        top_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.search_var = StringVar()
        self.search_entry = CTkEntry(
            top_frame,
            textvariable=self.search_var,
            width=400,
            placeholder_text="Search by vendor or contact person..."
        )
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_vendors())

        CTkButton(top_frame, text="🔄 Refresh", width=120, command=self.refresh_vendors).pack(side="left", padx=6)
        CTkButton(top_frame, text="⬅ Back", width=120, command=self.go_back).pack(side="right", padx=10)

        # ---------------- Scrollable Vendor List ----------------
        self.scroll_frame = CTkScrollableFrame(self.root, width=900, height=350, corner_radius=15)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # ---------------- Action Buttons ----------------
        action_frame = CTkFrame(self.root)
        action_frame.pack(pady=10)
        CTkButton(action_frame, text="➕ Add Vendor", width=160, command=self.open_add_window).grid(row=0, column=0, padx=10)
        CTkButton(action_frame, text="✏️ Edit Vendor", width=160, command=self.open_edit_window).grid(row=0, column=1, padx=10)
        CTkButton(action_frame, text="❌ Delete Vendor", width=160, command=self.delete_selected_vendor).grid(row=0, column=2, padx=10)

        # ---------------- Data Initialization ----------------
        self.vendors = []
        self.selected_vendor = None
        self.refresh_vendors()

        self.root.mainloop()

    # ---------------- Load All Vendors ----------------
    def refresh_vendors(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.vendors = get_all_vendors()
        if not self.vendors:
            CTkLabel(self.scroll_frame, text="No vendors found.", font=("Arial", 16, "italic")).pack(pady=20)
            return

        for vendor in self.vendors:
            card_text = (
                f"{vendor['vendor_name']} ({vendor['contact_person'] or 'No Contact'})\n"
                f"📧 {vendor['email'] or 'N/A'} | 📞 {vendor['phone'] or 'N/A'}"
            )

            btn = CTkButton(
                self.scroll_frame,
                text=card_text,
                width=850,
                height=70,
                anchor="w",
                font=("Arial", 14),
                command=lambda v=vendor: self.select_vendor(v)
            )
            btn.pack(pady=6, padx=10)

    # ---------------- Filter Vendors ----------------
    def filter_vendors(self):
        query = self.search_var.get().lower()
        filtered = [v for v in self.vendors if query in v["vendor_name"].lower() or (v.get("contact_person") and query in v["contact_person"].lower())]

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not filtered:
            CTkLabel(self.scroll_frame, text="No matching vendors.", font=("Arial", 16, "italic")).pack(pady=20)
            return

        for vendor in filtered:
            card_text = (
                f"{vendor['vendor_name']} ({vendor['contact_person'] or 'No Contact'})\n"
                f"📧 {vendor['email'] or 'N/A'} | 📞 {vendor['phone'] or 'N/A'}"
            )
            btn = CTkButton(
                self.scroll_frame,
                text=card_text,
                width=850,
                height=70,
                anchor="w",
                font=("Arial", 14),
                command=lambda v=vendor: self.select_vendor(v)
            )
            btn.pack(pady=6, padx=10)

    # ---------------- Select Vendor ----------------
    def select_vendor(self, vendor):
        self.selected_vendor = vendor
        messagebox.showinfo("Vendor Selected", f"Selected Vendor:\n{vendor['vendor_name']}")

    # ---------------- Add Vendor ----------------
    def open_add_window(self):
        self._open_vendor_form("Add New Vendor")

    # ---------------- Edit Vendor ----------------
    def open_edit_window(self):
        if not self.selected_vendor:
            messagebox.showwarning("Warning", "Please select a vendor to edit.")
            return
        self._open_vendor_form("Edit Vendor", self.selected_vendor)

    # ---------------- Add/Edit Form ----------------
    def _open_vendor_form(self, title, vendor=None):
        popup = CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("420x500")
        popup.resizable(False, False)
        popup.grab_set()
        popup.focus_force()

        fields = [
            ("Vendor Name", "vendor_name"),
            ("Contact Person", "contact_person"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Address", "address")
        ]

        entries = {}
        for label_text, key in fields:
            CTkLabel(popup, text=label_text, font=("Arial", 14)).pack(pady=(10, 0))
            entry = CTkEntry(popup, width=320)
            entry.pack(pady=5)
            if vendor:
                entry.insert(0, str(vendor.get(key, "")))
            entries[key] = entry

        def save_vendor():
            data = {key: entry.get().strip() for key, entry in entries.items()}
            if not data["vendor_name"]:
                messagebox.showerror("Error", "Vendor Name is required.")
                return

            if vendor:
                success = update_vendor(
                    vendor["vendor_id"],
                    data["vendor_name"],
                    data["contact_person"],
                    data["email"],
                    data["phone"],
                    data["address"]
                )
                msg = "updated"
            else:
                success = add_vendor(
                    data["vendor_name"],
                    data["contact_person"],
                    data["email"],
                    data["phone"],
                    data["address"]
                )
                msg = "added"

            if success:
                messagebox.showinfo("Success", f"Vendor {msg} successfully!")
                popup.destroy()
                self.refresh_vendors()
            else:
                messagebox.showerror("Error", f"Failed to {msg} vendor.")

        CTkButton(popup, text="💾 Save", width=200, command=save_vendor).pack(pady=20)

    # ---------------- Delete Vendor ----------------
    def delete_selected_vendor(self):
        if not self.selected_vendor:
            messagebox.showwarning("Warning", "Please select a vendor to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{self.selected_vendor['vendor_name']}'?")
        if not confirm:
            return

        success = delete_vendor(self.selected_vendor["vendor_id"])
        if success:
            messagebox.showinfo("Deleted", "Vendor deleted successfully.")
            self.refresh_vendors()
        else:
            messagebox.showerror("Error", "Failed to delete vendor.")

    # ---------------- Back to Dashboard ----------------
    def go_back(self):
        from Admin_Module.adminGUI import AdminGUI  # or Librarian_Module.librarianGUI if needed
        self.root.destroy()
        AdminGUI()
