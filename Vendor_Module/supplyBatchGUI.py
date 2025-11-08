# Vendor_Module/supplyBatchGUI.py
from customtkinter import *
from tkinter import messagebox
from Vendor_Module.vendorFunctionality import get_all_vendors, create_supply_batch
from Librarian_Module.manageBooksFunctionality import get_all_books

set_appearance_mode("dark")

class SupplyBatchGUI:
    def __init__(self, opened_by="Admin"):
        self.opened_by = opened_by
        self.root = CTk()
        self.root.title("📦 Create Supply Batch")
        self.root.geometry("950x650")
        self.root.minsize(800, 600)

        # ====== MAIN CONTAINER FRAME (SCROLLABLE CONTENT) ======
        main_scroll = CTkScrollableFrame(self.root, width=920, height=520, corner_radius=15)
        main_scroll.pack(fill="both", expand=True, padx=15, pady=(10, 0))

        # ---------------- TITLE ----------------
        CTkLabel(main_scroll, text="📦 Create New Supply Batch", font=("Arial", 22, "bold")).pack(pady=15)

        # ---------------- VENDOR SELECTION ----------------
        vendor_frame = CTkFrame(main_scroll)
        vendor_frame.pack(fill="x", padx=20, pady=(0, 10))

        CTkLabel(vendor_frame, text="Select Vendor:", font=("Arial", 16, "bold")).pack(side="left", padx=10)
        self.vendors = get_all_vendors()
        vendor_names = [v["vendor_name"] for v in self.vendors] if self.vendors else ["No Vendors Found"]
        self.vendor_var = StringVar(value=vendor_names[0])
        self.vendor_dropdown = CTkOptionMenu(vendor_frame, variable=self.vendor_var, values=vendor_names, width=300)
        self.vendor_dropdown.pack(side="left", padx=10)

        # ---------------- ADD BOOK SECTION ----------------
        CTkLabel(main_scroll, text="Add Books to Supply Batch", font=("Arial", 18, "bold")).pack(pady=(10, 0))

        book_frame = CTkFrame(main_scroll)
        book_frame.pack(fill="x", padx=20, pady=(5, 10))

        self.books = get_all_books()
        book_titles = [f"{b['title']} (ID: {b['b_Id']})" for b in self.books] if self.books else ["No Books Found"]

        CTkLabel(book_frame, text="Select Book:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
        self.book_var = StringVar(value=book_titles[0])
        self.book_dropdown = CTkOptionMenu(book_frame, variable=self.book_var, values=book_titles, width=350)
        self.book_dropdown.grid(row=0, column=1, padx=10, pady=5)

        CTkLabel(book_frame, text="Quantity:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5)
        self.qty_entry = CTkEntry(book_frame, width=150)
        self.qty_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        CTkLabel(book_frame, text="Cost Price (₹):", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5)
        self.cost_entry = CTkEntry(book_frame, width=150)
        self.cost_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        CTkButton(book_frame, text="➕ Add to Batch", width=150, command=self.add_book_to_batch).grid(row=3, column=1, pady=10, sticky="e")

        # ---------------- BOOKS ADDED LIST ----------------
        CTkLabel(main_scroll, text="Books in Current Batch:", font=("Arial", 16, "bold")).pack(pady=(5, 0))

        self.scroll_frame = CTkScrollableFrame(main_scroll, width=850, height=200, corner_radius=15)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # ---------------- FIXED BOTTOM BUTTONS ----------------
        bottom_frame = CTkFrame(self.root)
        bottom_frame.pack(fill="x", padx=20, pady=(5, 15))

        CTkButton(bottom_frame, text="💾 Save Batch", width=200, height=45, command=self.save_batch).pack(side="left", padx=20, pady=10)
        CTkButton(bottom_frame, text="⬅ Back", width=200, height=45, command=self.go_back).pack(side="right", padx=20, pady=10)

        # ---------------- INITIALIZE ----------------
        self.batch_items = []
        self.refresh_batch_items()

        self.root.mainloop()

    # ---------------- ADD BOOK ----------------
    def add_book_to_batch(self):
        if not self.books:
            messagebox.showerror("Error", "No books available to add.")
            return

        selected_book = self.book_var.get()
        selected = next((b for b in self.books if f"{b['title']} (ID: {b['b_Id']})" == selected_book), None)

        if not selected:
            messagebox.showerror("Error", "Invalid book selected.")
            return

        try:
            qty = int(self.qty_entry.get())
            cost = float(self.cost_entry.get())
            if qty <= 0 or cost <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter valid numeric values for Quantity and Cost.")
            return

        self.batch_items.append({
            "b_Id": selected["b_Id"],
            "title": selected["title"],
            "quantity": qty,
            "cost_price": cost
        })

        self.qty_entry.delete(0, "end")
        self.cost_entry.delete(0, "end")
        self.refresh_batch_items()

    # ---------------- DISPLAY ADDED BOOKS ----------------
    def refresh_batch_items(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not self.batch_items:
            CTkLabel(self.scroll_frame, text="No books added yet.", font=("Arial", 14, "italic")).pack(pady=20)
            return

        for item in self.batch_items:
            CTkLabel(
                self.scroll_frame,
                text=f"{item['title']} - Qty: {item['quantity']} | Cost: ₹{item['cost_price']:.2f}",
                font=("Arial", 14),
                anchor="w",
                justify="left"
            ).pack(fill="x", padx=10, pady=4)

    # ---------------- SAVE SUPPLY BATCH ----------------
    def save_batch(self):
        if not self.batch_items:
            messagebox.showwarning("Warning", "No books added to batch.")
            return

        vendor_name = self.vendor_var.get()
        vendor = next((v for v in self.vendors if v["vendor_name"] == vendor_name), None)
        if not vendor:
            messagebox.showerror("Error", "Invalid vendor selected.")
            return

        confirm = messagebox.askyesno("Confirm", f"Create supply batch for vendor '{vendor_name}'?")
        if not confirm:
            return

        success = create_supply_batch(vendor["vendor_id"], self.batch_items)
        if success:
            messagebox.showinfo("Success", "Supply batch created successfully (Status: Pending).")
            self.batch_items.clear()
            self.refresh_batch_items()
        else:
            messagebox.showerror("Error", "Failed to create supply batch.")

    # ---------------- GO BACK ----------------
    def go_back(self):
        confirm = messagebox.askyesno("Confirm", "Go back? Unsaved data will be lost.")
        if not confirm:
            return

        self.root.destroy()
        if self.opened_by.lower() == "librarian":
            from Librarian_Module.librarianGUI import LibrarianGUI
            LibrarianGUI()
        else:
            from Admin_Module.adminGUI import AdminGUI
            AdminGUI()
