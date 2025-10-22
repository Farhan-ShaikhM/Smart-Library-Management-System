from customtkinter import *
from tkinter import messagebox
from datetime import datetime
from Reader_Module.returnFunctionality import get_user_borrowed_books_with_dates, return_book
import re
set_appearance_mode("dark")

class ReturnGUI:
    def __init__(self, u_Id):
        self.u_Id = u_Id
        self.borrowed_books = get_user_borrowed_books_with_dates(self.u_Id)

        self.root = CTk()
        self.root.title("Return a Book")
        self.root.geometry("650x650")
        self.root.resizable(False, False)

        # ---------------- No books to return ----------------
        if not self.borrowed_books:
            CTkLabel(self.root, text="You have no books to return.", font=("Arial", 16, "bold")).pack(pady=50)
            CTkButton(self.root, text="Back", width=120, command=self.go_back).pack(pady=20)
            self.root.mainloop()
            return

        # ---------------- Book selection ----------------
        CTkLabel(self.root, text="Choose a book to return:", font=("Arial", 14, "bold")).pack(pady=(20, 5))
        self.book_var = StringVar()
        book_titles = [f"{b['title']} by {b['author']}" for b in self.borrowed_books]
        self.dropdown = CTkOptionMenu(self.root, variable=self.book_var, values=book_titles, width=400,anchor="n", command=self.update_book_details)
        self.dropdown.pack(pady=(0, 20))
        self.book_var.set(book_titles[0])

        # ---------------- Book details in left-aligned column ----------------
        details_frame = CTkFrame(self.root)
        details_frame.pack(pady=20, padx=20, fill="x")

        # Labels column
        label_frame = CTkFrame(details_frame)
        label_frame.pack(side="left", padx=20)
        CTkLabel(label_frame, text="Book Borrowed On:", font=("Arial", 12, "bold"), anchor="w").pack(pady=10,padx=20, fill="x")
        CTkLabel(label_frame, text="Due Date:", font=("Arial", 12, "bold"), anchor="w").pack(pady=10,padx=20, fill="x")
        CTkLabel(label_frame, text="Return Date:", font=("Arial", 12, "bold"), anchor="w").pack(pady=10,padx=20, fill="x")

        # Textboxes column
        textbox_frame = CTkFrame(details_frame)
        textbox_frame.pack(side="left", fill="x", expand=True)
        self.borrowed_on_text = CTkEntry(textbox_frame, width=200, font=("Arial", 12), state="disabled", justify="center")
        self.due_date_text = CTkEntry(textbox_frame, width=200, font=("Arial", 12), state="disabled", justify="center")
        self.return_date_text = CTkEntry(textbox_frame, width=200, font=("Arial", 12), state="disabled", justify="center")

        self.borrowed_on_text.pack(pady=10, fill="x")
        self.due_date_text.pack(pady=10, fill="x")
        self.return_date_text.pack(pady=10, fill="x")

        # Set Return Date
        self.return_date = datetime.now()
        self.return_date_text.configure(state="normal")
        self.return_date_text.delete(0, "end")
        self.return_date_text.insert(0, self.return_date.strftime('%Y-%m-%d'))
        self.return_date_text.configure(state="disabled")

        # ---------------- Rating ----------------
        CTkLabel(self.root, text="Your Rating (1-5):", font=("Arial", 12, "bold")).pack(pady=(10,5), anchor="n", padx=20)
        self.rating_var = StringVar()
        self.rating_entry = CTkEntry(self.root, textvariable=self.rating_var, width=50, font=("Arial", 12))
        self.rating_entry.pack(pady=(0,10), padx=20, anchor="n")

        # ---------------- Status ----------------
        CTkLabel(self.root, text="Return Status:", font=("Arial", 12, "bold")).pack(pady=(5, 5), anchor="n", padx=20)
        self.status_var = StringVar()
        self.status_dropdown = CTkOptionMenu(self.root, variable=self.status_var, values=["Returned", "Lost"], width=200, command=self.update_fine)
        self.status_dropdown.pack(pady=(0, 10), padx=20, anchor="n")
        self.status_var.set("Returned")

        # ---------------- Fine Label ----------------
        self.fine_label = CTkLabel(self.root, text="", font=("Arial", 18, "bold"))
        self.fine_label.pack(pady=(5, 10), padx=20, anchor="n")

        # ---------------- Buttons ----------------
        button_frame = CTkFrame(self.root)
        button_frame.pack(pady=10)
        CTkButton(button_frame, text="Return Book", width=150, command=self.return_selected_book).grid(row=0, column=0, padx=10)
        CTkButton(button_frame, text="Back", width=150, command=self.go_back).grid(row=0, column=1, padx=10)

        # Initial update
        self.update_book_details()

        self.root.mainloop()

    def update_book_details(self, choice=None):
        idx = self.dropdown.get()
        book = next((b for b in self.borrowed_books if f"{b['title']} by {b['author']}" == idx), None)
        if book:
            self.borrowed_on_text.configure(state="normal")
            self.borrowed_on_text.delete(0, "end")
            self.borrowed_on_text.insert(0, book['issue_date'].strftime('%Y-%m-%d'))
            self.borrowed_on_text.configure(state="disabled")

            self.due_date_text.configure(state="normal")
            self.due_date_text.delete(0, "end")
            self.due_date_text.insert(0, book['due_date'].strftime('%Y-%m-%d'))
            self.due_date_text.configure(state="disabled")

            self.update_fine()

    def update_fine(self, choice=None):
        idx = self.dropdown.get()
        book = next((b for b in self.borrowed_books if f"{b['title']} by {b['author']}" == idx), None)
        if not book:
            self.fine_label.configure(text="Total Fine: N/A")
            return

        status = self.status_var.get()
        if status == "Lost":
            fine = book.get('price', 0.0)
        else:
            days_overdue = (self.return_date.date() - book['due_date']).days
            fine = max(days_overdue, 0) * book.get('daily_late_fine', 0.5)

        self.fine_label.configure(text=f"Total Fine: {fine:.2f} units")

    def return_selected_book(self):
        idx = self.dropdown.get()
        book = next((b for b in self.borrowed_books if f"{b['title']} by {b['author']}" == idx), None)
        if not book:
            messagebox.showerror("Error", "Book not found!")
            return

        # Validate rating: allow 1-5, with max 1 decimal
        rating_input = self.rating_var.get()
        if not re.fullmatch(r"[1-4](\.\d)?|5(\.0)?", rating_input):
            messagebox.showerror("Error",
                                 "Please enter a rating between 1 and 5 with at most 1 decimal place (e.g., 4.5)")
            return

        rating = float(rating_input)

        status = self.status_var.get()
        success, fine_or_msg = return_book(self.u_Id, book['b_Id'], rating, status, self.return_date)
        if success:
            messagebox.showinfo("Success", f"Book processed successfully!\nTotal Fine: {fine_or_msg:.2f} units")
            self.root.destroy()
            self.go_back()
        else:
            messagebox.showerror("Error", f"Failed to process book: {fine_or_msg}")

    def go_back(self):
        from Reader_Module.readerGUI import ReaderGUI  # Avoid circular import
        self.root.destroy()
        ReaderGUI(self.u_Id)

