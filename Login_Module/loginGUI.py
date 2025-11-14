# Login_Module/loginGUI.py
from customtkinter import *
from tkinter import messagebox
from .loginFunctionality import DBAuth
from Registration_Module.registrationGUI import RegistrationGUI
from Reader_Module.readerGUI import ReaderGUI
from Librarian_Module.librarianGUI import LibrarianGUI
from Admin_Module.adminGUI import AdminGUI
from Vendor_Module.vendorGUI import VendorGUI
from Vendor_Module.vendorFunctionality import get_vendor_by_user_id

set_appearance_mode("dark")


class LoginGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x550")
        self.master.title("Login Page")
        self.master.resizable(0, 0)

        self.db = DBAuth()

        # ---------- Frame ----------
        self.login_frame = CTkFrame(self.master, width=340, height=400, corner_radius=20)
        self.login_frame.pack(pady=50)

        CTkLabel(self.login_frame, text="Welcome Back! Please Login", font=("Arial", 16)).pack(pady=20)
        CTkLabel(self.login_frame, text="👤", font=("Arial", 100)).pack(pady=(0, 20))

        # ---------- Entries ----------
        self.un_entry = CTkEntry(self.login_frame, placeholder_text="Enter Email", width=240, height=40)
        self.un_entry.pack()

        self.pw_entry = CTkEntry(self.login_frame, placeholder_text="Enter Password", width=240, height=40, show="*")
        self.pw_entry.pack(pady=20, padx=40)

        # ---------- Toggle visibility ----------
        self.toggle_button = CTkButton(
            self.login_frame, text="🐵", font=("Arial", 20),
            width=10, fg_color="transparent", hover=True, command=self.toggle_visibility
        )
        self.toggle_button.place(x=240, y=265)

        # ---------- Buttons ----------
        self.login_button = CTkButton(
            self.login_frame, text="Sign In", font=("Arial", 26),
            width=200, height=40, corner_radius=20, command=self.login_action
        )
        self.login_button.pack(pady=(10, 20))

        # ---------- Signup link ----------
        self.signup_text = CTkLabel(
            self.login_frame,
            text="Don't have an account? Sign up here",
            font=("Arial", 12),
            text_color="light blue",
            cursor="hand2"
        )
        self.signup_text.pack(pady=(0, 20))
        self.signup_text.bind("<Button-1>", self.open_registration)

    # ---------- Toggle password visibility ----------
    def toggle_visibility(self):
        if self.pw_entry.cget("show") == "*":
            self.pw_entry.configure(show="")
            self.toggle_button.configure(text="🙈")
        else:
            self.pw_entry.configure(show="*")
            self.toggle_button.configure(text="🐵")

    # ---------- Login Action ----------
    def login_action(self):
        email = self.un_entry.get().strip()
        password = self.pw_entry.get().strip()

        success, result = self.db.login(email, password)

        if success:
            self.master.destroy()
            role = result["role"]
            u_id = result["u_Id"]

            # ---------------- READER ----------------
            if role == "Reader":
                ReaderGUI(u_id)

            # ---------------- LIBRARIAN ----------------
            elif role == "Librarian":
                LibrarianGUI(u_id)

            # ---------------- ADMIN ----------------
            elif role == "Admin":
                AdminGUI(u_id)

            # ---------------- VENDOR ----------------
            elif role == "Vendor":
                vendor = get_vendor_by_user_id(u_id)
                if vendor:
                    VendorGUI(u_id, vendor["vendor_id"])  # ✅ pass both user ID and vendor ID
                else:
                    messagebox.showerror("Error", "No linked vendor record found for this user.")

            # ---------------- UNKNOWN ROLE ----------------
            else:
                messagebox.showerror("Error", f"Unknown user role: {role}")

        else:
            messagebox.showerror("Login Error", result)

    # ---------- Open Registration ----------
    def open_registration(self, event):
        self.master.destroy()
        RegistrationGUI()
