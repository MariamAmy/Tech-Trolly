import tkinter as tk
from tkinter import messagebox, font
import hashlib
import re

class SignUpPage(tk.Frame):
    """
    Represents the signup page of the Tech Trolley application.

    Attributes:
    - master: The master widget.
    - switch_to_login_callback: Callback function to switch to the login page.
    - db_conn: SQLite database connection.
    - admin: Boolean indicating whether the user signing up is an admin.
    """

    def __init__(self, master, switch_to_login_callback, db_conn, admin):
        """
        Initialize the SignUpPage.

        Parameters:
        - master: The master widget.
        - switch_to_login_callback: Callback function to switch to the login page.
        - db_conn: SQLite database connection.
        - admin: Boolean indicating whether the user signing up is an admin.
        """

        super().__init__(master)
        self.switch_to_login_callback = switch_to_login_callback
        self.db_conn = db_conn
        self.admin = admin
        self.configure(bg='#d9f4ff')
        self.create_widgets()

    def create_widgets(self):
        """
        Create and configure the widgets for the signup page.
        """

        # Create a frame to hold the sign-up widgets
        signup_frame = tk.Frame(self, bg='#ffffff', bd=2, relief='groove')
        signup_frame.grid(padx=50, pady=50)

        # Define the font styles
        title_font = font.Font(family="Arial", size=24, weight="bold")
        label_font = font.Font(family="Arial", size=14)
        entry_font = font.Font(family="Arial", size=12)
        button_font = font.Font(family="Arial", size=12, weight="bold")

        # Market name label
        self.label_tech_trolley = tk.Label(signup_frame, text="Tech Trolley", font=title_font, bg='#ffffff')
        self.label_tech_trolley.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # First Name Entry
        self.label_signup_firstname = tk.Label(signup_frame, text="First Name", font=label_font, bg='#ffffff')
        self.label_signup_firstname.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.entry_signup_firstname = tk.Entry(signup_frame, font=entry_font, width=25, bg='#f8f8f8')
        self.entry_signup_firstname.grid(row=1, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky='ew')

        # Last Name Entry
        self.label_signup_lastname = tk.Label(signup_frame, text="Last Name", font=label_font, bg='#ffffff')
        self.label_signup_lastname.grid(row=2, column=0, padx=20, pady=10, sticky='w')
        self.entry_signup_lastname = tk.Entry(signup_frame, font=entry_font, width=25, bg='#f8f8f8')
        self.entry_signup_lastname.grid(row=2, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky='ew')

        # Email Entry
        self.label_signup_email = tk.Label(signup_frame, text="Email", font=label_font, bg='#ffffff')
        self.label_signup_email.grid(row=3, column=0, padx=20, pady=10, sticky='w')
        self.entry_signup_email = tk.Entry(signup_frame, font=entry_font, width=25, bg='#f8f8f8')
        self.entry_signup_email.grid(row=3, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky='ew')

        # Password Entry
        self.label_signup_password = tk.Label(signup_frame, text="Password", font=label_font, bg='#ffffff')
        self.label_signup_password.grid(row=4, column=0, padx=20, pady=10, sticky='w')
        self.entry_signup_password = tk.Entry(signup_frame, show="*", font=entry_font, width=25, bg='#f8f8f8')
        self.entry_signup_password.grid(row=4, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky='ew')

        # Confirm Password Entry
        self.label_confirm_password = tk.Label(signup_frame, text="Confirm Password", font=label_font, bg='#ffffff')
        self.label_confirm_password.grid(row=5, column=0, padx=20, pady=10, sticky='w')
        self.entry_confirm_password = tk.Entry(signup_frame, show="*", font=entry_font, width=25, bg='#f8f8f8')
        self.entry_confirm_password.grid(row=5, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky='ew')

        # Phone Number Entry
        self.label_signup_phone = tk.Label(signup_frame, text="Phone Number", font=label_font, bg='#ffffff')
        self.label_signup_phone.grid(row=6, column=0, padx=20, pady=10, sticky='w')
        self.entry_signup_phone = tk.Entry(signup_frame, font=entry_font, width=25, bg='#f8f8f8')
        self.entry_signup_phone.grid(row=6, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky='ew')

        # Sign Up Button
        self.signup_button = tk.Button(signup_frame, text="Sign Up", command=self.signup, font=button_font)
        self.signup_button.grid(row=7, column=0, columnspan=2, pady=15)

        # Back to Login Button
        self.switch_to_login_button = tk.Button(signup_frame, text="Back to Login", command=self.switch_to_login_callback,
                                                 font=button_font)
        self.switch_to_login_button.grid(row=8, column=0, columnspan=2, pady=10)

        # If Admin, show "Add admin" option
        if self.admin:
            self.signup_button.configure(text="Add admin")

    def signup(self):
        """
        Handle the signup button click event.
        """

        email = self.entry_signup_email.get()
        password = self.entry_signup_password.get()
        confirm_password = self.entry_confirm_password.get()
        first_name = self.entry_signup_firstname.get()
        last_name = self.entry_signup_lastname.get()
        phone_number = self.entry_signup_phone.get()

        # Check for empty fields
        if not email or not password or not first_name or not last_name or not phone_number:
            messagebox.showerror("Sign up", "Please fill in all fields")
            return
        
        # Check if email is in the correct format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Sign Up", "Invalid email format")
            return
        
        # Check if password is at least 8 characters long
        if len(password) < 8:
            messagebox.showerror("Sign Up", "Password must be at least 8 characters long")
            return

        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Sign Up", "Password and Confirm Password do not match.")
            return
        
        # Check if phone number is in the correct format
        if not re.match(r"\+20(10|11|12|15)\d{8}", phone_number):
            messagebox.showerror("Sign Up", "Invalid phone number format (e.g., (+20)10xxxxxxxx)")
            return

        # Hash the password
        password = self.hash_password(password)

        # Insert user into the database
        with self.db_conn:
            cursor = self.db_conn.cursor()
            cursor.execute("INSERT INTO customers (email, password, first_name, last_name, phone_number, admin) \
                            VALUES (?, ?, ?, ?, ?, ?)",
                            (email, password, first_name, last_name, phone_number, self.admin if self.admin else False))
            self.db_conn.commit()

        # Show appropriate success message
        if self.admin:
            messagebox.showinfo("Sign Up", "Admin successfully registered.")
        else:
            messagebox.showinfo("Sign Up", "Account successfully registered.")

    def hash_password(self, password):
        """
        Hash the password using SHA-256.

        Parameters:
        - password: The password to be hashed.

        Returns:
        - str: The hashed password.
        """

        return hashlib.sha256(password.encode("utf-8")).hexdigest()