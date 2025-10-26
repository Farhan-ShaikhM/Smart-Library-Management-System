from customtkinter import *

class LibrarianGUI:
    def __init__(self):
        self.window = CTk()
        self.window.title("Librarian Dashboard")
        self.window.geometry("600x500")

        label = CTkLabel(self.window, text="Welcome, Librarian!", font=("Arial", 20))
        label.pack(pady=50)

        self.window.mainloop()
