from customtkinter import *
from tkinter import messagebox
from .loginFunctionality import DBAuth
from Registration_Module.registrationGUI import RegistrationGUI
from Reader_Module.readerGUI import ReaderGUI
from Librarian_Module.librarianGUI import LibrarianGUI
from Admin_Module.adminGUI import AdminGUI

set_appearance_mode("dark")

class LoginGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x550")
        self.master.title("Login Page")
        self.master.resizable(0,0)

        self.db = DBAuth()

        self.login_frame = CTkFrame(self.master, width=340, height=400, corner_radius=20)
        self.login_frame.pack(pady=50)

        self.welcome_text = CTkLabel(self.login_frame, text="Welcome Back user, Please Login", font=("arial", 16))
        self.welcome_text.pack(pady=20)

        self.user_logo = CTkLabel(self.login_frame, text="👤", font=("arial", 100))
        self.user_logo.pack(pady=(0, 20))

        self.un_entry = CTkEntry(self.login_frame, placeholder_text="Enter Email", width=240, height=40)
        self.un_entry.pack()

        self.pw_entry = CTkEntry(self.login_frame, placeholder_text="Enter Password", width=240, height=40, show="*")
        self.pw_entry.pack(pady=20, padx=40)

        self.toggle_button = CTkButton(self.login_frame, text="🐵", font=("arial", 20),
                                       width=10, fg_color="transparent", hover=True, command=self.toggle_visibility)
        self.toggle_button.place(x=240, y=265)

        self.login_button = CTkButton(self.login_frame, text="Sign In", font=("arial", 26),
                                      width=200, height=40, corner_radius=20,
                                      command=self.login_action)
        self.login_button.pack(pady=(10, 20))

        self.signup_text = CTkLabel(self.login_frame, text="Don't have an account already? Sign up here",
                                    font=("Arial", 12), text_color="light blue", cursor="hand2")
        self.signup_text.pack(pady=(0,20))
        self.signup_text.bind("<Button-1>", self.open_registration)

    def toggle_visibility(self):
        if self.pw_entry.cget("show") == "*":
            self.pw_entry.configure(show="")
            self.toggle_button.configure(text="🙈")
        else:
            self.pw_entry.configure(show="*")
            self.toggle_button.configure(text="🐵")

    def login_action(self):
        email = self.un_entry.get().strip()
        password = self.pw_entry.get().strip()

        success, result = self.db.login(email, password)
        if success:
            self.master.destroy()
            role = result['role']
            if role == "Reader":
                ReaderGUI()
            elif role == "Librarian":
                LibrarianGUI()
            elif role == "Admin":
                AdminGUI()
        else:
            messagebox.showerror("Login Error", result)

    def open_registration(self, event):
        self.master.destroy()
        RegistrationGUI()
