from customtkinter import *

class RegistrationGUI:
    def __init__(self):
        self.window = CTk()
        self.window.title("Registration Page")
        self.window.geometry("500x550")

        label = CTkLabel(self.window, text="Register New Account", font=("Arial", 20))
        label.pack(pady=50)

        # Example placeholder fields
        self.name_entry = CTkEntry(self.window, placeholder_text="Full Name", width=240, height=40)
        self.name_entry.pack(pady=10)

        self.email_entry = CTkEntry(self.window, placeholder_text="Email", width=240, height=40)
        self.email_entry.pack(pady=10)

        self.password_entry = CTkEntry(self.window, placeholder_text="Password", width=240, height=40, show="*")
        self.password_entry.pack(pady=10)

        self.register_button = CTkButton(self.window, text="Register", width=200, height=40)
        self.register_button.pack(pady=20)

        self.window.mainloop()
