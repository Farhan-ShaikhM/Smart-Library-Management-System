from customtkinter import *
from tkinter import messagebox
from Reader_Module.historyFunctionality import get_user_history
from datetime import datetime

set_appearance_mode("dark")

class HistoryGUI:
    def __init__(self, u_Id):
        self.u_Id = u_Id
        self.records = get_user_history(self.u_Id)

        # ---------------- Main window ----------------
        self.window = CTkToplevel()
        self.window.title("Borrowing History")
        self.window.geometry("700x600")
        self.window.resizable(False, False)

        # Bring window to front
        self.window.grab_set()
        self.window.focus_force()

        # ---------------- Scrollable frame ----------------
        self.scroll_frame = CTkScrollableFrame(self.window, width=680, height=420, corner_radius=15)
        self.scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # ---------------- Close button ----------------
        self.close_btn = CTkButton(self.window, text="Close", width=120, command=self.window.destroy)
        self.close_btn.pack(pady=(0, 10))

        self.display_history()

    # ---------------- Display history ----------------
    def display_history(self):
        if not self.records:
            CTkLabel(self.scroll_frame, text="No history available.", font=("Arial", 16, "italic")).pack(pady=20)
            return

        for rec in self.records:
            card = CTkFrame(self.scroll_frame, corner_radius=15,fg_color="gray")
            card.pack(fill="x", padx=10, pady=8)

            # Title and author
            title_label = CTkLabel(
                card,
                text=f"📚 {rec['title']} by {rec['author']}",
                font=("Arial", 16, "bold"),
                anchor="w",
                justify="left"
            )
            title_label.pack(fill="x", padx=10, pady=(10, 5))

            # Borrowed and returned dates
            borrowed_on = rec['issue_date'].strftime('%Y-%m-%d')
            returned_on = rec['return_date'].strftime('%Y-%m-%d') if rec['return_date'] else "Not Returned"
            details_text = (
                f"Borrowed On: {borrowed_on}\n"
                f"Returned On: {returned_on}\n"
                f"Due Date: {rec['due_date'].strftime('%Y-%m-%d')}\n"
                f"Status: {rec['loan_status']}\n"
                f"Fine Paid: {rec['fine_amount']:.2f} units\n"
                f"Returned On Time: {'Yes' if rec['return_date'] and rec['return_date'].date() <= rec['due_date'] else 'No'}"
            )
            details_label = CTkLabel(
                card,
                text=details_text,
                font=("Arial", 14),
                justify="left",
                anchor="w"
            )
            details_label.pack(fill="x", padx=10, pady=(0, 10))
