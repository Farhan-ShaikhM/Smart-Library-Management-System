# Librarian_Module/manageBooksGUI.py
from customtkinter import *
from tkinter import messagebox
from Librarian_Module.manageBooksFunctionality import get_all_books, add_new_book, update_book, delete_book

set_appearance_mode("dark")

class ManageBooksGUI:
    def __init__(self):
        self.root = CTk()
        self.root.title("📚 Manage Books")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)

        # ---------------- Title ----------------
        CTkLabel(self.root, text="📗 Manage Books", font=("Arial", 22, "bold")).pack(pady=15)

        # ---------------- Search + Control Buttons ----------------
        control_frame = CTkFrame(self.root)
        control_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.search_var = StringVar()
        self.search_entry = CTkEntry(control_frame, textvariable=self.search_var, width=400, placeholder_text="Search by title or author...")
        self.search_entry.pack(side="left", padx=(0,10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_books())

        CTkButton(control_frame, text="🔄 Refresh", width=120, command=self.refresh_books).pack(side="left", padx=10)
        CTkButton(control_frame, text="⬅ Back", width=120, command=self.go_back).pack(side="right", padx=10)

        # ---------------- Scrollable Frame ----------------
        self.scroll_frame = CTkScrollableFrame(self.root, width=950, height=400, corner_radius=15)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # ---------------- Action Buttons ----------------
        action_frame = CTkFrame(self.root)
        action_frame.pack(pady=10)
        CTkButton(action_frame, text="➕ Add Book", width=160, command=self.open_add_window).grid(row=0, column=0, padx=10)
        CTkButton(action_frame, text="✏️ Edit Book", width=160, command=self.open_edit_window).grid(row=0, column=1, padx=10)
        CTkButton(action_frame, text="❌ Delete Book", width=160, command=self.delete_selected_book).grid(row=0, column=2, padx=10)

        # ---------------- Load Books ----------------
        self.books = []
        self.selected_book = None
        self.refresh_books()

        self.root.mainloop()

    # ---------------- Refresh Book List ----------------
    def refresh_books(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.books = get_all_books()
        if not self.books:
            CTkLabel(self.scroll_frame, text="No books found.", font=("Arial", 16, "italic")).pack(pady=20)
            return

        for book in self.books:
            btn_text = (
                f"{book['title']} by {book['author']}\n"
                f"Genre: {book['main_genre']} | Stock: {book['available_stock']}/{book['total_stock']} | "
                f"Price: ₹{book['price']} | Fine/day: ₹{book['daily_late_fine']}"
            )
            btn = CTkButton(
                self.scroll_frame,
                text=btn_text,
                width=900,
                height=60,
                anchor="w",
                font=("Arial", 14),
                command=lambda b=book: self.select_book(b)
            )
            btn.pack(pady=6, padx=10)

    # ---------------- Filter Books ----------------
    def filter_books(self):
        query = self.search_var.get().lower()
        filtered = [b for b in self.books if query in b['title'].lower() or query in b['author'].lower()]

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not filtered:
            CTkLabel(self.scroll_frame, text="No matching books found.", font=("Arial", 16, "italic")).pack(pady=20)
            return

        for book in filtered:
            btn_text = (
                f"{book['title']} by {book['author']}\n"
                f"Genre: {book['main_genre']} | Stock: {book['available_stock']}/{book['total_stock']} | "
                f"Price: ₹{book['price']} | Fine/day: ₹{book['daily_late_fine']}"
            )
            btn = CTkButton(
                self.scroll_frame,
                text=btn_text,
                width=900,
                height=60,
                anchor="w",
                font=("Arial", 14),
                command=lambda b=book: self.select_book(b)
            )
            btn.pack(pady=6, padx=10)

    # ---------------- Select Book ----------------
    def select_book(self, book):
        self.selected_book = book
        messagebox.showinfo("Selected", f"Selected: {book['title']} by {book['author']}")

    # ---------------- Add Book ----------------
    def open_add_window(self):
    # Clear main content area
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        CTkLabel(self.scroll_frame, text="Add New Book", font=("Arial", 20, "bold")).pack(pady=10)

        fields = [
            ("Title", "title"),
            ("Author", "author"),
            ("Main Genre", "main_genre"),
            ("Sub Genre", "sub_genre"),
            ("Language", "language"),
            ("Total Stock", "total_stock"),
            ("Price (₹)", "price"),
            ("Daily Fine (₹)", "daily_late_fine")
        ]

        entries = {}
        for label_text, key in fields:
            CTkLabel(self.scroll_frame, text=label_text, font=("Arial", 14)).pack(pady=(5, 0))
            entry = CTkEntry(self.scroll_frame, width=400)
            entry.pack(pady=5)
            entries[key] = entry

        def save_book():
            data = {k: v.get().strip() for k, v in entries.items()}
            if any(v == "" for v in data.values()):
                messagebox.showerror("Error", "All fields are required.")
                return
            try:
                total_stock = int(data["total_stock"])
                price = float(data["price"])
                fine = float(data["daily_late_fine"])
            except ValueError:
                messagebox.showerror("Error", "Stock, Price, and Fine must be numeric.")
                return

            from Librarian_Module.manageBooksFunctionality import add_new_book
            success = add_new_book(
                data["title"], data["author"], data["main_genre"], data["sub_genre"],
                data["language"], total_stock, price, fine
            )

            if success:
                messagebox.showinfo("Success", "Book added successfully!")
                self.refresh_books()
            else:
                messagebox.showerror("Error", "Failed to add book.")

        CTkButton(self.scroll_frame, text="💾 Save Book", width=200, command=save_book).pack(pady=20)


    # ---------------- Edit Book ----------------
    def open_edit_window(self):
        if not self.selected_book:
            messagebox.showwarning("Warning", "Please select a book to edit.")
            return
        self._open_book_window("Edit Book", self.selected_book)

    # ---------------- Add/Edit Window ----------------
    def _open_book_window(self, title, book=None):
        popup = CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("420x600")
        popup.resizable(False, False)

        fields = [
            ("Title", "title"),
            ("Author", "author"),
            ("Main Genre", "main_genre"),
            ("Sub Genre", "sub_genre"),
            ("Language", "language"),
            ("Total Stock", "total_stock"),
            ("Price (₹)", "price"),
            ("Daily Fine (₹)", "daily_late_fine")
        ]

        entries = {}
        for label_text, key in fields:
            CTkLabel(popup, text=label_text, font=("Arial", 14)).pack(pady=(8, 0))
            entry = CTkEntry(popup, width=300)
            entry.pack(pady=4)
            if book:
                entry.insert(0, str(book.get(key, "")))
            entries[key] = entry

        def save_book():
            data = {key: entry.get().strip() for key, entry in entries.items()}
            if any(v == "" for v in data.values()):
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                total_stock = int(data["total_stock"])
                price = float(data["price"])
                fine = float(data["daily_late_fine"])
            except ValueError:
                messagebox.showerror("Error", "Stock, Price, and Fine must be numeric.")
                return

            if book:  # update
                success = update_book(
                    book["b_Id"],
                    data["title"], data["author"], data["main_genre"],
                    data["sub_genre"], data["language"],
                    total_stock, price, fine
                )
                msg = "updated"
            else:  # add
                success = add_new_book(
                    data["title"], data["author"], data["main_genre"],
                    data["sub_genre"], data["language"],
                    total_stock, price, fine
                )
                msg = "added"

            if success:
                messagebox.showinfo("Success", f"Book {msg} successfully.")
                popup.destroy()
                self.refresh_books()
            else:
                messagebox.showerror("Error", f"Failed to {msg} book.")

        CTkButton(popup, text="💾 Save", width=200, command=save_book).pack(pady=20)

    # ---------------- Delete Book ----------------
    def delete_selected_book(self):
        if not self.selected_book:
            messagebox.showwarning("Warning", "Please select a book first.")
            return

        confirm = messagebox.askyesno("Confirm", f"Delete '{self.selected_book['title']}'?")
        if not confirm:
            return

        success = delete_book(self.selected_book["b_Id"])
        if success:
            messagebox.showinfo("Success", "Book deleted successfully.")
            self.refresh_books()
        else:
            messagebox.showerror("Error", "Failed to delete book.")

    # ---------------- Back ----------------
    def go_back(self):
        from Librarian_Module.librarianGUI import LibrarianGUI
        self.root.destroy()
        LibrarianGUI()
