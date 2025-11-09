from datetime import date
from tkinter import messagebox

from customtkinter import *

from Admin_Module.registerVendorFunctionality import RegisterVendorFunctionality

try:
    from tkcalendar import DateEntry  # pip install tkcalendar
except ImportError:
    messagebox.showerror("Missing Dependency", "Please install tkcalendar:\n\npip install tkcalendar")
    raise SystemExit

set_appearance_mode("dark")


class RegisterVendorGUI:
    def __init__(self, u_id):
        self.u_Id = u_id
        self.window = CTk()
        self.window.title("Register New Vendor")
        self.window.geometry("520x740")
        self.window.resizable(0, 0)

        # DB helper
        self.db = RegisterVendorFunctionality(success_callback=self.show_success_screen)

        title_label = CTkLabel(self.window, text="Register New Vendor", font=("Arial", 20))
        title_label.pack(pady=25)

        # Full name
        self.name_entry = CTkEntry(self.window, placeholder_text="Full Name", width=360, height=40)
        self.name_entry.pack(pady=10)

        # Email
        self.email_entry = CTkEntry(self.window, placeholder_text="Email Address", width=360, height=40)
        self.email_entry.pack(pady=10)

        # Phone
        self.phone_entry = CTkEntry(self.window, placeholder_text="Phone Number (10 digits)", width=360, height=40)
        self.phone_entry.pack(pady=10)

        # Date of Birth
        dob_frame = CTkFrame(self.window)
        dob_frame.pack(pady=10)
        CTkLabel(dob_frame, text="Date of Birth:", font=("Arial", 13)).pack(anchor="w", padx=8)

        self.dob_widget = DateEntry(
            dob_frame,
            width=18,
            year=date.today().year - 30,
            date_pattern='yyyy-mm-dd'
        )
        self.dob_widget.pack(padx=8, pady=6)

        # Address (optional)
        self.address_entry = CTkEntry(self.window, placeholder_text="Address (optional)", width=360, height=40)
        self.address_entry.pack(pady=10)

        # Password
        self.password_entry = CTkEntry(self.window, placeholder_text="Password", width=360, height=40, show="*")
        self.password_entry.pack(pady=10)

        # Confirm password
        self.confirm_entry = CTkEntry(self.window, placeholder_text="Confirm Password", width=360, height=40, show="*")
        self.confirm_entry.pack(pady=10)

        # Register button
        self.register_button = CTkButton(
            self.window,
            text="Register Vendor",
            width=260,
            height=40,
            command=self.register_action
        )
        self.register_button.pack(pady=20)

        # Back to admin (cancel) button
        self.back_button = CTkButton(
            self.window,
            text="Cancel",
            width=180,
            height=36,
            command=self.go_back
        )
        self.back_button.pack(pady=(4, 20))

        self.window.mainloop()

    def get_dob(self):
        """Return a date object or None"""
        try:
            return self.dob_widget.get_date()
        except Exception:
            return None

    def register_action(self):
        full_name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_entry.get().strip()
        dob = self.get_dob()

        # Register as librarian (includes DOB validation)
        self.db.register_vendor(full_name, email, password, confirm_password, phone, address, dob)

    def show_success_screen(self):
        # Close registration window and show success
        try:
            if hasattr(self, "window") and self.window.winfo_exists():
                self.window.destroy()
        except Exception:
            pass

        success_window = CTk()
        success_window.title("Registration Successful")
        success_window.geometry("420x300")
        success_window.resizable(0, 0)

        label = CTkLabel(success_window, text="🎉 Vendor Registered!", font=("Arial", 22))
        label.pack(pady=40)

        desc = CTkLabel(success_window, text="The Vendor account has been created successfully.", font=("Arial", 14))
        desc.pack(pady=10)

        back_btn = CTkButton(success_window, text="⬅ Back to Admin Panel", width=200, height=40,
                             command=lambda: self._close_and_return_to_admin(success_window))
        back_btn.pack(pady=20)

        success_window.mainloop()

    def _close_and_return_to_admin(self, win):
        try:
            win.destroy()
        except Exception:
            pass
        from Admin_Module.adminGUI import AdminGUI
        AdminGUI(self.u_Id)

    def go_back(self):
        try:
            if hasattr(self, "window") and self.window.winfo_exists():
                self.window.destroy()
        except Exception:
            pass
        from Admin_Module.adminGUI import AdminGUI
        AdminGUI(self.u_Id)
