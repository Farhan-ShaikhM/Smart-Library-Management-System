from customtkinter import *
from tkinter import messagebox
import threading
import os
from openai import OpenAI
from Reader_Module.borrowFunctionality import get_available_books, get_user_borrowed_books, borrow_book_for_user

set_appearance_mode("dark")


class BorrowGUI:
    def __init__(self, u_Id):
        self.u_Id = u_Id

        # ---------------- Main window ----------------
        self.root = CTk()
        self.root.title("Borrow a Book")
        self.root.geometry("950x600")
        self.root.resizable(False, False)

        # ---------------- Search bar ----------------
        self.search_frame = CTkFrame(self.root, corner_radius=15)
        self.search_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.search_var = StringVar()
        self.search_entry = CTkEntry(
            self.search_frame,
            textvariable=self.search_var,
            placeholder_text="Search books...",
            width=850,
            height=40,
            font=("Arial", 14)
        )
        self.search_entry.pack(side="left", padx=(10, 0), pady=10, expand=True, fill="x")
        self.search_entry.bind("<KeyRelease>", self.filter_books)

        self.search_icon = CTkLabel(
            self.search_frame,
            text="🔍",
            font=("Arial", 20),
            width=40
        )
        self.search_icon.pack(side="right", padx=10)

        # ---------------- Scrollable frame ----------------
        self.scroll_frame = CTkScrollableFrame(self.root, width=900, height=450, corner_radius=15)
        self.scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # ---------------- Back button ----------------
        self.back_button = CTkButton(
            self.root,
            text="⬅ Back to Home",
            width=200,
            height=40,
            font=("Arial", 16, "bold"),
            command=self.back_to_home
        )
        self.back_button.pack(pady=(0, 10))

        # ---------------- Load books ----------------
        self.books = get_available_books()
        self.borrowed_books = get_user_borrowed_books(self.u_Id)  # List of borrowed b_Id
        self.display_books(self.books)

        self.root.mainloop()

    # ---------------- Filter books ----------------
    def filter_books(self, event=None):
        query = self.search_var.get().lower()
        filtered = [book for book in self.books if query in book["title"].lower() or query in book["author"].lower()]
        self.display_books(filtered)

    # ---------------- Display book cards ----------------
    def display_books(self, books):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not books:
            CTkLabel(self.scroll_frame, text="No books found.", font=("Arial", 16, "italic")).pack(pady=20)
            return

        for book in books:
            card = CTkFrame(self.scroll_frame, corner_radius=15)
            card.pack(fill="x", padx=20, pady=10)

            # -------- Title --------
            title_label = CTkLabel(
                card,
                text=book["title"],
                font=("Arial", 18, "bold"),
                anchor="w",
                justify="left"
            )
            title_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

            # -------- Author, Genre, Rating, Stock --------
            details_text = (
                f"Author: {book['author']}\n"
                f"Genre: {book['main_genre']}\n"
                f"Rating: {book['aggregate_rating']} / 5\n"
                f"Available: {book['available_stock']}"
            )
            details_label = CTkLabel(
                card,
                text=details_text,
                font=("Arial", 14),
                justify="left",
                anchor="w"
            )
            details_label.grid(row=1, column=0, sticky="w", padx=15, pady=5)

            # -------- See Summary --------
            summary_label = CTkLabel(
                card,
                text="📘 See Summary",
                font=("Arial", 14, "underline"),
                text_color="#1E90FF",
                cursor="hand2"
            )
            summary_label.grid(row=2, column=0, sticky="w", padx=15, pady=(5, 10))
            summary_label.bind("<Button-1>", lambda e, b=book: self.show_summary_window(b))

            # -------- Borrow Button --------
            already_borrowed = book["b_Id"] in self.borrowed_books
            borrow_btn = CTkButton(
                card,
                text="Already Borrowed" if already_borrowed else "Borrow",
                width=140,
                height=35,
                font=("Arial", 14, "bold"),
                state="disabled" if already_borrowed else "normal",
                fg_color="#555555" if already_borrowed else None,
                hover_color="#444444" if already_borrowed else None,
                command=(None if already_borrowed else lambda b=book: self.borrow_book(b))
            )
            borrow_btn.grid(row=2, column=1, sticky="e", padx=15, pady=(5, 10))

            card.grid_columnconfigure(0, weight=1)
            card.grid_columnconfigure(1, weight=0)

    # ---------------- Borrow book ----------------
    def borrow_book(self, book):
        result = borrow_book_for_user(self.u_Id, book["b_Id"])
        if result:
            messagebox.showinfo("Success", f"You successfully borrowed '{book['title']}'!")
            self.borrowed_books = get_user_borrowed_books(self.u_Id)
            self.display_books(self.books)
        else:
            messagebox.showerror("Error", f"Failed to borrow '{book['title']}'.")

    # ---------------- Show summary popup ----------------
    def show_summary_window(self, book):
        popup = CTkToplevel(self.root)
        popup.title(f"{book['title']} Summary")
        popup.geometry("600x400")
        popup.resizable(False, False)
        popup.grab_set()
        popup.focus_force()

        CTkLabel(
            popup,
            text=f"📖 {book['title']} by {book['author']}",
            font=("Arial", 18, "bold"),
            wraplength=550,
            justify="center"
        ).pack(pady=(15, 10), padx=10)

        scrollable_frame = CTkScrollableFrame(popup, corner_radius=10)
        scrollable_frame.pack(padx=15, pady=10, fill="both", expand=True)

        summary_label = CTkLabel(
            scrollable_frame,
            text="Loading summary, please wait...",
            font=("Arial", 14),
            wraplength=520,
            justify="left"
        )
        summary_label.pack(padx=10, pady=10, anchor="nw")

        CTkButton(popup, text="Close", width=100, command=popup.destroy).pack(pady=(5, 10))

        threading.Thread(
            target=self.fetch_summary_from_groq,
            args=(book, summary_label),
            daemon=True
        ).start()

    # ---------------- Update summary label ----------------
    def update_summary_textbox(self, label_widget, text):
        label_widget.configure(text=text)

    # ---------------- Fetch summary via Groq API ----------------
    def fetch_summary_from_groq(self, book, textbox):
        try:
            api_key = "Your api key"
            client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

            user_prompt = (
                f"Pretend you are an AI model based for handling books and reply only on the following prompt:\n"
                f"Give me a summary in 2-3 paragraphs for the book '{book['title']}' by {book['author']}.\n"
                f"If you don’t have a summary for the book just say 'no summary found...'\n"
                f"Don’t say anything else."
            )

            response = client.responses.create(input=user_prompt, model="openai/gpt-oss-20b")
            summary = response.output_text.strip() if hasattr(response, "output_text") else "No summary found..."
        except Exception as e:
            summary = f"⚠️ Error fetching summary:\n{e}"

        textbox.after(0, lambda: self.update_summary_textbox(textbox, summary))

    # ---------------- Back to Reader Dashboard ----------------
    def back_to_home(self):
        from Reader_Module.readerGUI import ReaderGUI  # Local import avoids circular import
        self.root.destroy()
        ReaderGUI(self.u_Id)
