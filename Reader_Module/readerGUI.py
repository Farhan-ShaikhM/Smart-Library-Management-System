from customtkinter import *

class ReaderGUI:
    def __init__(self):
        self.window = CTk()
        self.window.title("Reader Dashboard")
        self.window.geometry("1000x600")
        self.window.resizable(0,0)

        label = CTkLabel(self.window, text="Welcome, Reader!", font=("Arial", 20))
        label.pack(pady=50)

        # Placeholder for Reader functionalities (borrowed books, fines, etc.)

        self.window.mainloop()

#r1 = ReaderGUI()