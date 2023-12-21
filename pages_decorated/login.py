import tkinter as tk
from tkinter import messagebox, font
import hashlib

class LoginPage(tk.Frame):
    """
    Represents the login page of the Tech Trolley application.

    Attributes:
    - master: The master widget.
    - switch_to_signup_callback: Callback function to switch to the signup page.
    - switch_to_home_callback: Callback function to switch to the home page.
    - db_conn: SQLite database connection.
    """

    def __init__(self, master, switch_to_signup_callback, switch_to_home_callback, db_conn):
        """
        Initialize the LoginPage.

        Parameters:
        - master: The master widget.
        - switch_to_signup_callback: Callback function to switch to the signup page.
        - switch_to_home_callback: Callback function to switch to the home page.
        - db_conn: SQLite database connection.
        """

        super().__init__(master)
        self.master = master
        self.grid_forget()
        self.switch_to_signup_callback = switch_to_signup_callback
        self.switch_to_home_callback = switch_to_home_callback
        self.db_conn = db_conn
        self.configure(bg="#d9f4ff")
        self.create_widgets()

    def create_widgets(self):
        """
        Create and configure the widgets for the login page.
        """

        # Create a frame to hold the login widgets
        login_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="groove")
        login_frame.grid(padx=50, pady=50)

        # Configure the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Define the font styles
        title_font = font.Font(family="Arial", size=24, weight="bold")
        label_font = font.Font(family="Arial", size=14)
        entry_font = font.Font(family="Arial", size=12)
        button_font = font.Font(family="Arial", size=12, weight="bold")

        # Market name label
        self.market_name_label = tk.Label(login_frame, text="Tech Trolley", font=title_font, bg="#ffffff")
        self.market_name_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Email Entry
        self.label_email = tk.Label(login_frame, text="Email", font=label_font, bg="#ffffff")
        self.label_email.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.entry_email = tk.Entry(login_frame, font=entry_font, width=25, bg="#f8f8f8")
        self.entry_email.grid(row=1, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky="ew")

        # Password Entry
        self.label_password = tk.Label(login_frame, text="Password", font=label_font, bg="#ffffff")
        self.label_password.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.entry_password = tk.Entry(login_frame, show="*", font=entry_font, width=25, bg="#f8f8f8")
        self.entry_password.grid(row=2, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky="ew")

        # Login Button
        self.login_button = tk.Button(login_frame, text="Login", command=self.login, font=button_font)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=15)

        # Signup Button
        self.signup_button = tk.Button(login_frame, text="Sign Up", command=self.switch_to_signup_callback, font=button_font)
        self.signup_button.grid(row=4, column=0, columnspan=2, pady=10)

    def login(self):
        """
        Handle the login button click event.
        """

        email = self.entry_email.get()
        password = self.entry_password.get()

        # Check for empty fields
        if not email or not password:
            messagebox.showerror("Log in", "Please fill in all fields")
            return

        # Check user credentials in the database
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE email=? AND password=?", (email, self.hash_password(password)))
        result = cursor.fetchone()

        # If credentials are valid, switch to the home page
        if result:
            cursor.execute("SELECT admin FROM customers WHERE email=? AND password=?", (email, self.hash_password(password)))
            admin = cursor.fetchone()[0]
            self.master.email = email
            self.master.admin = admin
            self.switch_to_home_callback()
        else:
            messagebox.showerror("Login", "Invalid email or password")

    def hash_password(self, password):
        """
        Hash the password using SHA-256.

        Parameters:
        - password: The password to be hashed.

        Returns:
        - str: The hashed password.
        """
        
        return hashlib.sha256(password.encode("utf-8")).hexdigest()