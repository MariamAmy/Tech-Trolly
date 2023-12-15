import tkinter as tk
from tkinter import messagebox
import hashlib

class LoginPage(tk.Frame):
    def __init__(self, master, switch_to_signup_callback, switch_to_home_callback, db_conn):
        super().__init__(master)
        self.master = master
        self.grid_forget()  # Initially hide the sign-up frame
        self.switch_to_signup_callback = switch_to_signup_callback
        self.switch_to_home_callback = switch_to_home_callback
        self.create_widgets()
        self.db_conn = db_conn

    def create_widgets(self):
        self.label_email = tk.Label(self, text="Email")
        self.label_email.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.entry_email = tk.Entry(self)
        self.entry_email.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.label_password = tk.Label(self, text="Password")
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.signup_button = tk.Button(self, text="Sign Up", 
                                       command=lambda admin = False: self.switch_to_signup_callback(admin))
        self.signup_button.grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        if not email:
            messagebox.showerror("Login", "Email is empty")
            return

        if not password:
            messagebox.showerror("Login", "Password is empty")
            return

        with self.db_conn:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT * FROM customers WHERE email=? AND password=?", (email, self.hash_password(password)))
            result = cursor.fetchone()

        if result:
            self.switch_to_home_callback()
        else:
            messagebox.showerror("Login", "Invalid email or password")

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()