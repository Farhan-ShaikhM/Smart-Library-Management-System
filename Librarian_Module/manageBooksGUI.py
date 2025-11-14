# Librarian_Module/manageBooksGUI.py
from customtkinter import *
from tkinter import messagebox
from Librarian_Module.manageBooksFunctionality import (
    get_all_books, add_book, update_book, delete_book
)

set_appearance_mode("dark")


class ManageBooksGUI:
    def __init__(self, u_Id):
        self.u_Id = u_Id
        self.root = CTk()
        self.root.title("📚 Manage Books")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)

        # ---------- Title ----------
        CTkLabel(self.root, text="📘 Manage Books", font=("Arial", 24, "bold")).pack(pady=20)

        # ---------- Buttons ----------
        CTkButton(self.root, text="➕ Add New Book", width=180, command=self.add_book_window).pack(pady=10)
        CTkButton(self.root, text="⬅ Back", width=180, command=self.go_back).pack(pady=10)

        # ---------- Book List ----------
        self.scroll_frame = CTkScrollableFrame(self.root, width=900, height=450)
        self.scroll_frame.pack(pady=10)

        self.load_books()

        self.root.mainloop()

    # ---------- Load Books ----------
    def load_books(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        books = get_all_books()
        if not books:
            CTkLabel(self.scroll_frame, text="No books found.", font=("Arial", 14, "italic")).pack(pady=20)
            return

        for b in books:
            book_info = (
                f"📕 {b['title']} by {b['author']}\n"
                f"Genre: {b['main_genre']} | Lang: {b['language'] or 'Unknown'} | "
                f"Stock: {b['available_stock']}/{b['total_stock']} | ₹{b['price'] or 0.0}"
            )

            frame = CTkFrame(self.scroll_frame, corner_radius=10)
            frame.pack(fill="x", pady=5, padx=10)

            CTkLabel(frame, text=book_info, font=("Arial", 14), justify="left").pack(side="left", padx=10)
            CTkButton(frame, text="✏ Edit", width=100, command=lambda bid=b['b_Id']: self.edit_book_window(bid)).pack(side="right", padx=5)
            CTkButton(frame, text="🗑 Delete", width=100, fg_color="red", command=lambda bid=b['b_Id']: self.remove_book(bid)).pack(side="right", padx=5)

    # ---------- Add New Book ----------
    def add_book_window(self):
        win = CTkToplevel(self.root)
        win.title("Add New Book")
        win.geometry("400x500")

        fields = ["Title", "Author", "Main Genre", "Sub Genre", "Language", "Stock", "Price"]
        entries = {}
        for f in fields:
            CTkLabel(win, text=f, font=("Arial", 14)).pack(pady=(10, 0))
            entries[f] = CTkEntry(win, width=300)
            entries[f].pack(pady=5)

        def save_book():
            title = entries["Title"].get().strip()
            author = entries["Author"].get().strip()
            genre = entries["Main Genre"].get().strip()
            sub_genre = entries["Sub Genre"].get().strip()
            language = entries["Language"].get().strip()
            stock = entries["Stock"].get().strip()
            price = entries["Price"].get().strip()

            if not (title and author and stock.isdigit()):
                messagebox.showerror("Error", "Please enter valid details.")
                return

            if add_book(title, author, genre, sub_genre, language, int(stock), float(price or 0)):
                messagebox.showinfo("Success", "Book added successfully!")
                win.destroy()
                self.load_books()
            else:
                messagebox.showerror("Error", "Failed to add book.")

        CTkButton(win, text="💾 Save", command=save_book).pack(pady=20)

    # ---------- Edit Existing Book ----------
    def edit_book_window(self, b_Id):
        import mysql.connector
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="slms_db")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books WHERE b_Id=%s", (b_Id,))
        b = cursor.fetchone()
        conn.close()

        if not b:
            messagebox.showerror("Error", "Book not found.")
            return

        win = CTkToplevel(self.root)
        win.title("Edit Book")
        win.geometry("400x500")

        fields = {
            "Title": b["title"],
            "Author": b["author"],
            "Main Genre": b["main_genre"],
            "Sub Genre": b["sub_genre"],
            "Language": b["language"],
            "Stock": str(b["available_stock"]),
            "Price": str(b["price"]),
        }

        entries = {}
        for f, val in fields.items():
            CTkLabel(win, text=f, font=("Arial", 14)).pack(pady=(10, 0))
            e = CTkEntry(win, width=300)
            e.insert(0, val if val else "")
            e.pack(pady=5)
            entries[f] = e

        def save_changes():
            title = entries["Title"].get().strip()
            author = entries["Author"].get().strip()
            genre = entries["Main Genre"].get().strip()
            sub_genre = entries["Sub Genre"].get().strip()
            language = entries["Language"].get().strip()
            stock = entries["Stock"].get().strip()
            price = entries["Price"].get().strip()

            if not (title and author and stock.isdigit()):
                messagebox.showerror("Error", "Invalid data.")
                return

            if update_book(b_Id, title, author, genre, sub_genre, language, int(stock), float(price or 0)):
                messagebox.showinfo("Success", "Book updated successfully!")
                win.destroy()
                self.load_books()
            else:
                messagebox.showerror("Error", "Failed to update book.")

        CTkButton(win, text="💾 Save Changes", command=save_changes).pack(pady=20)

    # ---------- Delete ----------
    def remove_book(self, b_Id):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this book?")
        if not confirm:
            return

        if delete_book(b_Id):
            messagebox.showinfo("Success", "Book deleted successfully!")
            self.load_books()
        else:
            messagebox.showerror("Error", "Failed to delete book.")

    # ---------- Back ----------
    def go_back(self):
        from Librarian_Module.librarianGUI import LibrarianGUI
        self.root.destroy()
        LibrarianGUI(self.u_Id)
