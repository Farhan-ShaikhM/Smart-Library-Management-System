from customtkinter import *

class AdminGUI:
    def __init__(self):
        self.window = CTk()
        self.window.title("Admin Dashboard")
        self.window.geometry("600x500")

        label = CTkLabel(self.window, text="Welcome, Admin!", font=("Arial", 20))
        label.pack(pady=50)
        self.window.mainloop()
#dummy comment