from customtkinter import *
from .registrationFunctionality import RegistrationFunctionality

class RegistrationGUI:
    def __init__(self):
        self.window = CTk()
        self.window.title("Registration Page")
        self.window.geometry("500x650")
        self.window.resizable(0, 0)

        self.db = RegistrationFunctionality(success_callback=self.show_success_screen)

        title_label = CTkLabel(self.window, text="Register New Account", font=("Arial", 20))
        title_label.pack(pady=30)

        self.name_entry = CTkEntry(self.window, placeholder_text="Full Name", width=300, height=40)
        self.name_entry.pack(pady=10)

        self.email_entry = CTkEntry(self.window, placeholder_text="Email Address", width=300, height=40)
        self.email_entry.pack(pady=10)

        self.phone_entry = CTkEntry(self.window, placeholder_text="Phone Number", width=300, height=40)
        self.phone_entry.pack(pady=10)

        self.password_entry = CTkEntry(self.window, placeholder_text="Password", width=300, height=40, show="*")
        self.password_entry.pack(pady=10)

        self.confirm_entry = CTkEntry(self.window, placeholder_text="Confirm Password", width=300, height=40, show="*")
        self.confirm_entry.pack(pady=10)

        self.register_button = CTkButton(self.window, text="Register", width=200, height=40, command=self.register_action)
        self.register_button.pack(pady=20)

        self.window.mainloop()

    def register_action(self):
        full_name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_entry.get().strip()

        self.db.register_user(full_name, email, password, confirm_password, phone)

    def show_success_screen(self):
        self.window.destroy()
        success_window = CTk()
        success_window.title("Registration Successful")
        success_window.geometry("400x300")
        success_window.resizable(0, 0)

        label = CTkLabel(success_window, text="🎉 Registration Successful!", font=("Arial", 22))
        label.pack(pady=50)

        desc = CTkLabel(success_window, text="You can now log in to your account.", font=("Arial", 16))
        desc.pack(pady=10)

        login_btn = CTkButton(success_window, text="Back to Login", width=180, height=40, command=lambda: self.go_to_login(success_window))
        login_btn.pack(pady=30)

        success_window.mainloop()

    def go_to_login(self, window):
        from Login_Module.loginGUI import LoginGUI
        window.destroy()
        root = CTk()
        app = LoginGUI(root)
        root.mainloop()
