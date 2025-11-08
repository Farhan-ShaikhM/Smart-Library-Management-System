# Admin_Module/manageBooksGUI.py
from decimal import Decimal
from customtkinter import *
from tkinter import messagebox

from Admin_Module.manageBooksFunctionality import (
    get_all_books, get_book_by_id, update_book, insert_book, delete_book
)

set_appearance_mode("dark")


class ManageBooksGUI:
    def __init__(self, u_Id=None):
        self.u_Id = u_Id
        self.root = CTk()
        self.root.title("Manage Books")
        self.root.geometry("950x600")
        self.root.resizable(False, False)

        # Main container
        self.main_frame = CTkFrame(self.root, corner_radius=12)
        self.main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Header row: title + back + add button + search
        header = CTkFrame(self.main_frame)
        header.pack(fill="x", pady=(0, 8))

        CTkLabel(header, text="Manage Books", font=("Arial", 22, "bold")).pack(side="left", padx=(6, 0))

        right_actions = CTkFrame(header)
        right_actions.pack(side="right", padx=(0, 6))

        CTkButton(right_actions, text="⬅ Back", width=120, command=self.go_back).pack(side="right", padx=(6, 0))
        CTkButton(right_actions, text="➕ Add New Book", width=160, command=self.open_add_book).pack(side="right", padx=(6, 0))

        # Search row
        search_row = CTkFrame(self.main_frame)
        search_row.pack(fill="x", pady=(0, 10), padx=(6, 6))

        self.search_var = StringVar()
        self.search_entry = CTkEntry(
            search_row,
            textvariable=self.search_var,
            placeholder_text="Search books by title or author...",
            width=600,
            height=36,
            font=("Arial", 14)
        )
        self.search_entry.pack(side="left", padx=(6, 8), pady=2, fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_books())

        search_icon = CTkLabel(search_row, text="🔍", font=("Arial", 18))
        search_icon.pack(side="right", padx=(0, 8))

        # Scrollable list of books
        self.scroll_frame = CTkScrollableFrame(self.main_frame, corner_radius=12)
        self.scroll_frame.pack(fill="both", expand=True, padx=6, pady=6)

        # initial load
        self.load_books()

        self.root.mainloop()

    def go_back(self):
        try:
            from Admin_Module.adminGUI import AdminGUI
            self.root.destroy()
            AdminGUI(self.u_Id)
        except Exception as e:
            messagebox.showerror("Error", f"Could not go back: {e}", parent=self.root)

    def load_books(self):
        # Clear existing children
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        raw_books = get_all_books() or []
        query = self.search_var.get().strip().lower()
        if query:
            books = [
                b for b in raw_books
                if query in (b.get('title') or '').lower() or query in (b.get('author') or '').lower()
            ]
        else:
            books = raw_books

        if not books:
            CTkLabel(self.scroll_frame, text="No books found.", font=("Arial", 16)).pack(pady=20)
            return

        for book in books:
            row = CTkFrame(self.scroll_frame, corner_radius=15, fg_color="gray")
            row.pack(fill="x", padx=10, pady=8)

            left = CTkFrame(row, fg_color="gray")
            left.pack(side="left", fill="both", padx=10, pady=10, expand=True)

            # Title: bigger and bolder
            title_label = CTkLabel(
                left,
                text=book.get("title", "Untitled"),
                font=("Arial", 18, "bold"),
                anchor="w",
                justify="left"
            )
            title_label.pack(fill="x", padx=10, pady=(8, 2))

            # Info lines (one per line)
            info_parts = [
                f"Author: {book.get('author', 'Unknown')}",
                f"Main Genre: {book.get('main_genre') or '-'}",
                f"Sub Genre: {book.get('sub_genre') or '-'}",
                f"Language: {book.get('language') or '-'}",
                f"Available Stock: {book.get('available_stock', 0)}",
                f"Total Stock: {book.get('total_stock', 0)}",
                f"Price: ₹{book.get('price', 0)}",
                f"Aggregate Rating: {book.get('aggregate_rating', 0)} / 5",
                f"Daily Late Fine: ₹{book.get('daily_late_fine', 0.0)}"
            ]
            info_text = "\n".join(info_parts)
            meta_label = CTkLabel(left, text=info_text, font=("Arial", 13), anchor="w", justify="left")
            meta_label.pack(fill="x", padx=12, pady=(0, 2))

            btns = CTkFrame(row, fg_color="gray")
            btns.pack(side="right", padx=12, pady=12)

            manage_btn = CTkButton(btns, text="Manage Book", width=140, command=lambda b_id=book['b_Id']: self.open_manage_book(b_id))
            manage_btn.pack(pady=(0, 6))
            del_btn = CTkButton(
                btns,
                text="Delete",
                width=100,
                fg_color="#b22222",
                hover_color="#9a1a1a",
                command=lambda b_id=book['b_Id'], t=book.get('title'): self.delete_book_confirm(b_id, t)
            )
            del_btn.pack(fill="both")

    def open_manage_book(self, b_Id):
        book = get_book_by_id(b_Id)
        if not book:
            messagebox.showerror("Error", "Could not fetch book details.", parent=self.root)
            return
        ManageBookDetailWindow(self, book)

    def open_add_book(self):
        AddBookWindow(self)

    def delete_book_confirm(self, b_Id, title):
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{title}'? This cannot be undone.", parent=self.root):
            return
        success, err = delete_book(b_Id)
        if success:
            messagebox.showinfo("Deleted", "Book deleted successfully.", parent=self.root)
            self.load_books()
        else:
            messagebox.showerror("Delete Failed", f"Could not delete book:\n{err}", parent=self.root)


class ManageBookDetailWindow:
    def __init__(self, parent_gui: ManageBooksGUI, book: dict):
        self.parent = parent_gui
        self.book = book

        # Create Toplevel so parent ManageBooksGUI remains open
        self.win = CTkToplevel(self.parent.root)
        self.win.title(f"Edit: {book.get('title')}")
        self.win.geometry("700x620")
        self.win.resizable(False, False)

        # Make sure this window stays on top and grabs focus
        try:
            self.win.attributes("-topmost", True)
        except Exception:
            pass
        self.win.focus_force()
        self.win.grab_set()

        # Container
        container = CTkFrame(self.win, corner_radius=12)
        container.pack(fill="both", expand=True, padx=12, pady=12)

        CTkLabel(container, text="Edit Book Details", font=("Arial", 20, "bold")).pack(pady=(4, 10))

        form = CTkFrame(container)
        form.pack(fill="both", expand=True, padx=6, pady=6)

        def add_field(label_text, initial_value, row_no, width=440):
            lbl = CTkLabel(form, text=label_text, font=("Arial", 13))
            lbl.grid(row=row_no, column=0, sticky="w", padx=(6, 6), pady=(8, 2))
            ent = CTkEntry(form, width=width)
            ent.grid(row=row_no, column=1, sticky="w", padx=(6, 6), pady=(8, 2))
            ent.insert(0, "" if initial_value is None else str(initial_value))
            return ent

        # Fields
        self.title_ent = add_field("Title", book.get("title"), 0)
        self.author_ent = add_field("Author", book.get("author"), 1)
        self.main_genre_ent = add_field("Main Genre", book.get("main_genre"), 2)
        self.sub_genre_ent = add_field("Sub Genre", book.get("sub_genre"), 3)
        self.language_ent = add_field("Language", book.get("language"), 4)
        self.available_stock_ent = add_field("Available Stock", book.get("available_stock"), 5)
        self.total_stock_ent = add_field("Total Stock", book.get("total_stock"), 6)
        self.price_ent = add_field("Price (₹)", book.get("price"), 7)
        self.aggregate_rating_ent = add_field("Aggregate Rating (0.0 - 5.0)", book.get("aggregate_rating"), 8)
        self.daily_late_fine_ent = add_field("Daily Late Fine (₹)", book.get("daily_late_fine"), 9)

        btn_frame = CTkFrame(container)
        btn_frame.pack(fill="x", pady=(10, 0), padx=6)

        save_btn = CTkButton(btn_frame, text="Save", width=140, command=self.save_changes)
        save_btn.pack(side="right", padx=(8, 12))

        cancel_btn = CTkButton(btn_frame, text="Cancel", width=120, command=self.close)
        cancel_btn.pack(side="right", padx=(8, 0))

    def close(self):
        try:
            if self.win.winfo_exists():
                self.win.destroy()
        except Exception:
            pass

    # helpers that attach parent for messageboxes
    def show_error(self, title, msg):
        messagebox.showerror(title, msg, parent=self.win)

    def show_info(self, title, msg):
        messagebox.showinfo(title, msg, parent=self.win)

    def save_changes(self):
        data = {}
        data["title"] = self.title_ent.get().strip()
        data["author"] = self.author_ent.get().strip()
        data["main_genre"] = self.main_genre_ent.get().strip() or None
        data["sub_genre"] = self.sub_genre_ent.get().strip() or None
        data["language"] = self.language_ent.get().strip() or None

        # Validate numeric fields
        try:
            av = int(self.available_stock_ent.get().strip())
            tot = int(self.total_stock_ent.get().strip())
            if av < 0 or tot <= 0 or tot < av:
                raise ValueError("Stock counts invalid (ensure 0 <= available <= total).")
            data["available_stock"] = av
            data["total_stock"] = tot
        except Exception as e:
            self.show_error("Validation Error", f"Stock values invalid:\n{e}")
            return

        try:
            price = Decimal(self.price_ent.get().strip())
            if price < 0:
                raise ValueError("Price must be >= 0")
            data["price"] = price
        except Exception as e:
            self.show_error("Validation Error", f"Price invalid:\n{e}")
            return

        try:
            rating = Decimal(self.aggregate_rating_ent.get().strip())
            if rating < 0 or rating > 5:
                raise ValueError("Rating must be between 0.0 and 5.0")
            rating = rating.quantize(Decimal("0.1"))
            data["aggregate_rating"] = rating
        except Exception as e:
            self.show_error("Validation Error", f"Aggregate rating invalid:\n{e}")
            return

        try:
            daily = Decimal(self.daily_late_fine_ent.get().strip())
            if daily < 0:
                raise ValueError("Daily late fine must be >= 0")
            data["daily_late_fine"] = daily
        except Exception as e:
            self.show_error("Validation Error", f"Daily late fine invalid:\n{e}")
            return

        success, err = update_book(self.book["b_Id"], data)
        if success:
            self.show_info("Success", "Book updated successfully.")
            try:
                self.parent.load_books()
            except Exception:
                pass
            self.close()
        else:
            self.show_error("Database Error", f"Failed to update book:\n{err}")


class AddBookWindow:
    def __init__(self, parent: ManageBooksGUI):
        self.parent = parent
        self.win = CTkToplevel(self.parent.root)
        self.win.title("Add New Book")
        self.win.geometry("700x620")
        self.win.resizable(False, False)

        # Keep window on top and focused
        try:
            self.win.attributes("-topmost", True)
        except Exception:
            pass
        self.win.focus_force()
        self.win.grab_set()

        container = CTkFrame(self.win, corner_radius=12)
        container.pack(fill="both", expand=True, padx=12, pady=12)

        CTkLabel(container, text="Add New Book", font=("Arial", 20, "bold")).pack(pady=(4, 10))

        form = CTkFrame(container)
        form.pack(fill="both", expand=True, padx=6, pady=6)

        def add_field(label_text, initial_value, row_no, width=440):
            lbl = CTkLabel(form, text=label_text, font=("Arial", 13))
            lbl.grid(row=row_no, column=0, sticky="w", padx=(6, 6), pady=(8, 2))
            ent = CTkEntry(form, width=width)
            ent.grid(row=row_no, column=1, sticky="w", padx=(6, 6), pady=(8, 2))
            if initial_value is not None:
                ent.insert(0, str(initial_value))
            return ent

        self.title_ent = add_field("Title", "", 0)
        self.author_ent = add_field("Author", "", 1)
        self.main_genre_ent = add_field("Main Genre", "", 2)
        self.sub_genre_ent = add_field("Sub Genre", "", 3)
        self.language_ent = add_field("Language", "", 4)
        self.available_stock_ent = add_field("Available Stock", "1", 5)
        self.total_stock_ent = add_field("Total Stock", "1", 6)
        self.price_ent = add_field("Price (₹)", "0.00", 7)
        self.aggregate_rating_ent = add_field("Aggregate Rating (0.0 - 5.0)", "0.0", 8)
        self.daily_late_fine_ent = add_field("Daily Late Fine (₹)", "10.00", 9)

        btn_frame = CTkFrame(container)
        btn_frame.pack(fill="x", pady=(10, 0), padx=6)

        save_btn = CTkButton(btn_frame, text="Add Book", width=140, command=self.add_book)
        save_btn.pack(side="right", padx=(8, 12))

        cancel_btn = CTkButton(btn_frame, text="Cancel", width=120, command=self.close)
        cancel_btn.pack(side="right", padx=(8, 0))

    def show_error(self, title, msg):
        messagebox.showerror(title, msg, parent=self.win)

    def show_info(self, title, msg):
        messagebox.showinfo(title, msg, parent=self.win)

    def close(self):
        try:
            if self.win.winfo_exists():
                self.win.destroy()
        except Exception:
            pass

    def add_book(self):
        data = {}
        data["title"] = self.title_ent.get().strip()
        data["author"] = self.author_ent.get().strip()
        if not data["title"] or not data["author"]:
            self.show_error("Validation", "Title and Author are required.")
            return

        data["main_genre"] = self.main_genre_ent.get().strip() or None
        data["sub_genre"] = self.sub_genre_ent.get().strip() or None
        data["language"] = self.language_ent.get().strip() or None

        try:
            av = int(self.available_stock_ent.get().strip())
            tot = int(self.total_stock_ent.get().strip())
            if av < 0 or tot <= 0 or tot < av:
                raise ValueError("Stock counts invalid (ensure 0 <= available <= total).")
            data["available_stock"] = av
            data["total_stock"] = tot
        except Exception as e:
            self.show_error("Validation Error", f"Stock values invalid:\n{e}")
            return

        try:
            price = Decimal(self.price_ent.get().strip())
            if price < 0:
                raise ValueError("Price must be >= 0")
            data["price"] = price
        except Exception as e:
            self.show_error("Validation Error", f"Price invalid:\n{e}")
            return

        try:
            rating = Decimal(self.aggregate_rating_ent.get().strip())
            if rating < 0 or rating > 5:
                raise ValueError("Rating must be between 0.0 and 5.0")
            rating = rating.quantize(Decimal("0.1"))
            data["aggregate_rating"] = rating
        except Exception as e:
            self.show_error("Validation Error", f"Aggregate rating invalid:\n{e}")
            return

        try:
            daily = Decimal(self.daily_late_fine_ent.get().strip())
            if daily < 0:
                raise ValueError("Daily late fine must be >= 0")
            data["daily_late_fine"] = daily
        except Exception as e:
            self.show_error("Validation Error", f"Daily late fine invalid:\n{e}")
            return

        success, res = insert_book(data)
        if success:
            self.show_info("Success", "Book added successfully.")
            try:
                self.parent.load_books()
            except Exception:
                pass
            self.close()
        else:
            self.show_error("Database Error", f"Failed to add book:\n{res}")

c1 = ManageBooksGUI()