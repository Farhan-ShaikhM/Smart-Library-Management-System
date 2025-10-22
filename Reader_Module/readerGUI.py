from customtkinter import *
from tkinter import messagebox

from Reader_Module.readerFunctionality import get_reader_data, return_book, get_recommendations

set_appearance_mode("dark")

class ReaderGUI:
    def __init__(self, u_Id):
        # Fetch reader data from database
        self.reader_data = get_reader_data(u_Id)
        if not self.reader_data:
            messagebox.showerror("Error", "Could not fetch reader data.")
            return

        # ---------------- Main window ----------------
        self.root = CTk()
        self.root.title("Reader Dashboard")
        self.root.geometry("950x600")
        self.root.resizable(0, 0)

        # ---------------- Main container ----------------
        self.main_frame = CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------------- Left column ----------------
        self.left_frame = CTkFrame(self.main_frame, width=250, corner_radius=15)
        self.left_frame.pack(side="left", fill="y", padx=(10,5), pady=10)

        self.welcome_frame = CTkFrame(self.left_frame, width=250, corner_radius=15)
        self.welcome_frame.pack(fill = "both",padx=10,pady=10)

        # User emoji
        self.user_logo = CTkLabel(self.welcome_frame, text="👤", font=("Arial", 100))
        self.user_logo.pack(pady=(20, 10))

        #Welcome label
        self.welcome_label = CTkLabel(
            self.welcome_frame,
            text=f"Welcome,\n{self.reader_data['full_name']}",
            font=("Arial", 18, "bold"),
            justify="center"
        )
        self.welcome_label.pack(pady=(0, 10), padx=20)

        self.remark_frame = CTkFrame(self.left_frame, width=250, corner_radius=15)
        self.remark_frame.pack(fill="both", padx=10, pady=(0,10))

        # User remark
        self.remark_label = CTkLabel(
            self.remark_frame,
            text=f"Remark:\n",
            font=("Arial", 18, "bold"),
            justify="center",
            wraplength=200
        )
        self.remark_label.pack(pady=(20,0), padx=20)

        self.user_remark_label = CTkLabel(
            self.remark_frame,
            text=f"{self.reader_data.get('remark', 'No remarks')}",
            font=("Arial", 14),
            justify="center",
            wraplength=200
        )
        self.user_remark_label.pack(pady=(0,20), padx=20)

        # ---------------- Right area ----------------
        self.right_frame = CTkFrame(self.main_frame, corner_radius=15)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

        # -------- Stats frames at top --------
        self.stats_frame = CTkFrame(self.right_frame, corner_radius=15)
        self.stats_frame.pack(pady=(10, 20))

        card_size = 150

        # Container to hold cards
        self.stats_container = CTkFrame(self.stats_frame, corner_radius=0)
        self.stats_container.pack()

        # Books Read Card
        self.books_read_card = CTkFrame(self.stats_container, width=card_size, height=card_size, corner_radius=15)
        self.books_read_card.pack(side="left", padx=10)
        self.books_read_card.pack_propagate(False)
        self.books_read_label = CTkLabel(
            self.books_read_card,
            text=f"Total Books Read:\n{self.reader_data['total_books_read']}",
            font=("Arial", 16),
            justify="center",
            anchor="center"
        )
        self.books_read_label.pack(expand=True, padx=10, pady=10)

        # Fines Card
        self.fines_card = CTkFrame(self.stats_container, width=card_size, height=card_size, corner_radius=15)
        self.fines_card.pack(side="left", padx=10)
        self.fines_card.pack_propagate(False)
        self.fines_label = CTkLabel(
            self.fines_card,
            text=f"Total Fines (₹):\n{self.reader_data['total_fines']:.2f}",
            font=("Arial", 16),
            justify="center",
            anchor="center"
        )
        self.fines_label.pack(expand=True, padx=10, pady=10)

        # Active Loans Card
        self.active_loans_card = CTkFrame(self.stats_container, width=card_size, height=card_size, corner_radius=15)
        self.active_loans_card.pack(side="left", padx=10)
        self.active_loans_card.pack_propagate(False)
        self.active_loans_label = CTkLabel(
            self.active_loans_card,
            text=f"Active Loans:\n{self.reader_data['active_loans']}",
            font=("Arial", 16),
            justify="center",
            anchor="center"
        )
        self.active_loans_label.pack(expand=True, padx=10, pady=10)

        # -------- Buttons frame --------
        self.buttons_frame = CTkFrame(self.right_frame, corner_radius=15)
        self.buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        btn_width = 300
        btn_height = 60

        self.action_label = CTkLabel(self.buttons_frame,
                                     text="⚡ Quick Actions:",
                                     font=("Arial", 18, "bold"),
                                     justify="center",
                                     anchor="center")
        self.action_label.pack(side="top", padx=10, pady=10)

        self.borrow_btn = CTkButton(
            self.buttons_frame,
            text="📖 Borrow a Book",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=lambda: self.borrow_book()
        )
        self.borrow_btn.pack(pady=20)

        self.return_btn = CTkButton(
            self.buttons_frame,
            text="📦 Return a Book",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=lambda: self.return_book()
        )
        self.return_btn.pack(pady=20)

        self.recommend_btn = CTkButton(
            self.buttons_frame,
            text="💡 Show Recommendations",
            font=("Arial", 18, "bold"),
            width=btn_width,
            height=btn_height,
            command=lambda: self.show_recommendations()
        )
        self.recommend_btn.pack(pady=20)

        self.root.mainloop()

    # ---------------- Functional buttons ----------------
    def borrow_book(self):
        from Reader_Module.borrowGUI import BorrowGUI  # ✅ local import avoids circular issue
        self.root.destroy()
        BorrowGUI(self.reader_data['u_Id'])

    def return_book(self):
        u_Id = self.reader_data['u_Id']
        return_book(u_Id, loan_id=None)
        messagebox.showinfo("Return", "Return Book feature coming soon!")

    def show_recommendations(self):
        u_Id = self.reader_data['u_Id']
        recommendations = get_recommendations(u_Id)
        messagebox.showinfo("Recommendations", "Recommendations feature coming soon!")
