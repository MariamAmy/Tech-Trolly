import tkinter as tk
from tkinter import messagebox
import hashlib

class SignUpPage(tk.Frame):
    def __init__(self, master, switch_to_login_callback, db_conn, admin):
        super().__init__(master)
        self.grid_forget()
        self.create_widgets(switch_to_login_callback)
        self.db_conn = db_conn
        self.admin = admin

    def create_widgets(self, switch_to_login_callback):
        self.label_signup_firstname = tk.Label(self, text="First Name")
        self.label_signup_firstname.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.entry_signup_firstname = tk.Entry(self)
        self.entry_signup_firstname.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.label_signup_lastname = tk.Label(self, text="Last Name")
        self.label_signup_lastname.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.entry_signup_lastname = tk.Entry(self)
        self.entry_signup_lastname.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        self.label_signup_email = tk.Label(self, text="Email")
        self.label_signup_email.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.entry_signup_email = tk.Entry(self)
        self.entry_signup_email.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        self.label_signup_password = tk.Label(self, text="Password")
        self.label_signup_password.grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.entry_signup_password = tk.Entry(self, show="*")
        self.entry_signup_password.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        self.label_confirm_password = tk.Label(self, text="Confirm Password")
        self.label_confirm_password.grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.entry_confirm_password = tk.Entry(self, show="*")
        self.entry_confirm_password.grid(row=4, column=1, padx=10, pady=5, sticky='w')

        self.label_signup_phone = tk.Label(self, text="Phone Number")
        self.label_signup_phone.grid(row=5, column=0, padx=10, pady=5, sticky='w')
        self.entry_signup_phone = tk.Entry(self)
        self.entry_signup_phone.grid(row=5, column=1, padx=10, pady=5, sticky='w')

        self.signup_button = tk.Button(self, text="Sign Up", command=self.signup)
        self.signup_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.switch_to_login_button = tk.Button(self, text="Back to Login", command=switch_to_login_callback)
        self.switch_to_login_button.grid(row=7, column=0, columnspan=2, pady=10)

    def signup(self):
        email = self.entry_signup_email.get()
        password = self.entry_signup_password.get()

        confirm_password = self.entry_confirm_password.get()
        if password != confirm_password:
            messagebox.showerror("Sign Up", "Password and Confirm Password do not match.")
            return
        else:
            messagebox.showinfo("Sign Up", "Account seccussfully resgistered.")
        password = self.hash_password(password)
        first_name = self.entry_signup_firstname.get()
        last_name = self.entry_signup_lastname.get()
        phone_number = self.entry_signup_phone.get()

        if not email:
            messagebox.showerror("Sign up", "Email is empty")
            return

        if not password:
            messagebox.showerror("Sign up", "Password is empty")
            return
        
        if not first_name:
            messagebox.showerror("Sign up", "First Name is empty")
            return
        
        if not last_name:
            messagebox.showerror("Sign up", "Last Name is empty")
            return
        
        if not phone_number:
            messagebox.showerror("Sign up", "Phone Number is empty")
            return
        

        with self.db_conn:
            cursor = self.db_conn.cursor()

            # Insert the new entry into the customers table
            cursor.execute("INSERT INTO customers (email, password, first_name, last_name, phone_number) VALUES (?, ?, ?, ?, ?, ?)",
                        (email, password, first_name, last_name, phone_number, self.admin))

            # Commit the changes and close the database connection
            self.db_conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
