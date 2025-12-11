# Librarian_Module/requestBooksGUI.py
from customtkinter import *
from tkinter import messagebox
from Librarian_Module.requestBooksFunctionality import (
    get_all_vendors, get_librarian_requests, send_book_request
)

set_appearance_mode("dark")


class RequestBooksGUI:
    def __init__(self, u_Id):
        self.u_Id = u_Id
        self.root = CTk()
        self.root.title("📘 Request Books")
        self.root.geometry("950x650")
        self.root.resizable(False, False)

        # ---------- Header ----------
        CTkLabel(self.root, text="📚 Request New Books", font=("Arial", 24, "bold")).pack(pady=20)

        # ---------- Vendor Dropdown ----------
        vendors = get_all_vendors()
        self.vendor_map = {v["company"]: v["vendor_id"] for v in vendors}
        vendor_names = list(self.vendor_map.keys()) or ["No Vendors"]

        vendor_frame = CTkFrame(self.root)
        vendor_frame.pack(pady=10)
        CTkLabel(vendor_frame, text="Select Vendor:", font=("Arial", 14)).pack(side="left", padx=10)
        self.vendor_var = StringVar(value=vendor_names[0])
        self.vendor_menu = CTkOptionMenu(vendor_frame, variable=self.vendor_var, values=vendor_names)
        self.vendor_menu.pack(side="left", padx=10)

        # ---------- Form ----------
        form = CTkFrame(self.root)
        form.pack(pady=10)

        CTkLabel(form, text="Book Title:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.title_entry = CTkEntry(form, width=300)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        CTkLabel(form, text="Author:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.author_entry = CTkEntry(form, width=300)
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)

        CTkLabel(form, text="Quantity:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.qty_entry = CTkEntry(form, width=100)
        self.qty_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # ---------- Buttons ----------
        btn_frame = CTkFrame(self.root)
        btn_frame.pack(pady=15)
        CTkButton(btn_frame, text="📤 Submit Request", width=200, height=40,
                  command=self.submit_request).pack(side="left", padx=15)
        CTkButton(btn_frame, text="⬅ Back", width=150, height=40,
                  command=self.go_back).pack(side="left", padx=15)

        # ---------- Request List ----------
        CTkLabel(self.root, text="📜 Your Book Requests", font=("Arial", 18, "bold")).pack(pady=(10, 5))
        self.scroll_frame = CTkScrollableFrame(self.root, width=880, height=300, corner_radius=15)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.refresh_requests()
        self.root.mainloop()

    # ---------- Submit Request ----------
    def submit_request(self):
        vendor_name = self.vendor_var.get()
        vendor_id = self.vendor_map.get(vendor_name, None)
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        qty = self.qty_entry.get().strip()

        if not (vendor_id and title and qty.isdigit()):
            messagebox.showerror("Error", "Enter valid title, quantity, and vendor.")
            return

        if send_book_request(self.u_Id, vendor_id, title, author, int(qty)):
            messagebox.showinfo("Success", "Book request sent successfully!")
            self.title_entry.delete(0, "end")
            self.author_entry.delete(0, "end")
            self.qty_entry.delete(0, "end")
            self.refresh_requests()
        else:
            messagebox.showerror("Error", "Failed to send request.")

    # ---------- Load Requests ----------
    def refresh_requests(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        requests = get_librarian_requests(self.u_Id)
        if not requests:
            CTkLabel(self.scroll_frame, text="No requests found.",
                     font=("Arial", 14, "italic")).pack(pady=20)
            return

        for r in requests:
            info = (
                f"📘 {r['book_title']} by {r['author'] or 'Unknown'}\n"
                f"Qty: {r['quantity']} | Vendor: {r['vendor_name']}\n"
                f"Status: {r['status']} | Date: {r['request_date']}"
            )
            CTkLabel(self.scroll_frame, text=info, font=("Arial", 14),
                     justify="left", anchor="w").pack(fill="x", padx=15, pady=8)

    # ---------- Back ----------
    def go_back(self):
        from Librarian_Module.librarianGUI import LibrarianGUI
        self.root.destroy()
        LibrarianGUI(self.u_Id)
