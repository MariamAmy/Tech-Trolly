import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re 

class PaymentPage(tk.Frame):
    def __init__(self, master, switch_to_cart_callback, db_conn, cart_id, total_price, N_cart_items):
        super().__init__(master)
        self.db_conn = db_conn
        self.cart_id = cart_id
        self.total_price = total_price
        self.N_cart_items = N_cart_items
        self.visa = 0
        self.grid(row=0, column=0, sticky="nsew")
        self.configure_grid()
        self.grid_forget()
        self.create_widgets(switch_to_cart_callback)

    def create_widgets(self, switch_to_cart_callback):
        # Frame for the Home button at the top left
        self.home_frame = tk.Frame(self)
        self.home_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.button_home = tk.Button(self.home_frame, text="Home", command=self.on_home_click)
        self.button_home.pack(side="left", padx=5, pady=5)

        self.top_right_frame = tk.Frame(self)
        self.top_right_frame.grid(row=0, column=2, sticky="ne", padx=10, pady=10)

        # Create the cart button and place it in the top_right_frame
        self.button_cart = tk.Button(self.top_right_frame, compound = "bottom", text = self.N_cart_items
                                     , command=switch_to_cart_callback)
        self.button_cart.pack(padx=5, pady=5)

        # Center frame for the other widgets
        self.center_frame = tk.Frame(self)
        # Place center_frame in the middle cell of the grid
        self.center_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        # Create widgets in the center frame
        self.create_center_widgets()

    def create_center_widgets(self):
        # Widgets in the center of the screen
        self.label_promo_code = tk.Label(self.center_frame, text="Promo code")
        self.label_promo_code.grid(row=0, column=0, pady=5, sticky='w')
        self.entry_promo_code = tk.Entry(self.center_frame)
        self.entry_promo_code.grid(row=0, column=1, pady=5, sticky='w')

        self.label_payment_method = tk.Label(self.center_frame, text="Payment method")
        self.label_payment_method.grid(row=1, column=0, pady=5, sticky='w')
        self.payment_method_var = tk.StringVar()
        self.payment_method_options = ['Credit Card', 'Debit Card', 'Cash on Delivery']
        self.optionmenu_payment_method = ttk.Combobox(self.center_frame, textvariable=self.payment_method_var, values=self.payment_method_options)
        self.optionmenu_payment_method.grid(row=1, column=1, pady=5, sticky='w')
        self.optionmenu_payment_method.bind("<<ComboboxSelected>>", self.on_payment_method_changed)

        self.label_visa = tk.Label(self.center_frame, text="Visa Number")
        self.label_visa.grid(row=2, column=0, pady=5, sticky='w')
        self.entry_visa_number = tk.Entry(self.center_frame)
        self.entry_visa_number.grid(row=2, column=1, pady=5, sticky='w')

        self.label_expiry_date = tk.Label(self.center_frame, text="Expiry Date (MM/YY)")
        self.label_expiry_date.grid(row=3, column=0, pady=5, sticky='w')
        self.entry_expiry_date = tk.Entry(self.center_frame)
        self.entry_expiry_date.grid(row=3, column=1, pady=5, sticky='w')

        self.label_cvv = tk.Label(self.center_frame, text="CVV")
        self.label_cvv.grid(row=4, column=0, pady=5, sticky='w')
        self.entry_cvv = tk.Entry(self.center_frame, show="*")
        self.entry_cvv.grid(row=4, column=1, pady=5, sticky='w')

        self.label_visa.grid_remove()
        self.entry_visa_number.grid_remove()
        self.label_expiry_date.grid_remove()
        self.entry_expiry_date.grid_remove()
        self.label_cvv.grid_remove()
        self.entry_cvv.grid_remove()
        
        self.label_address = tk.Label(self.center_frame, text="Address")
        self.label_address.grid(row=5, column=0, pady=5, sticky='w')
        self.entry_address = tk.Entry(self.center_frame)
        self.entry_address.grid(row=5, column=1, pady=5, sticky='w')

        self.button_payment = tk.Button(self.center_frame, text="Payment", command=self.confirm_payment)
        self.button_payment.grid(row=6, column=0, columnspan=2, pady=10)

    def configure_grid(self):
        # Configure the grid to center the center_frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def on_home_click(self):
        pass

    def on_payment_method_changed(self, event=None):
        payment_method = self.payment_method_var.get()
        if payment_method in ['Credit Card', 'Debit Card']:
            self.label_visa.grid()
            self.entry_visa_number.grid()
            self.label_expiry_date.grid()
            self.entry_expiry_date.grid()
            self.label_cvv.grid()
            self.entry_cvv.grid()
            self.visa = 1
        else:
            self.label_visa.grid_remove()
            self.entry_visa_number.grid_remove()
            self.label_expiry_date.grid_remove()
            self.entry_expiry_date.grid_remove()
            self.label_cvv.grid_remove()
            self.entry_cvv.grid_remove()
            self.visa = 0

    def validate_payment(self):
        visa_number = self.entry_visa_number.get()
        if self.is_valid_visa_number(visa_number):
            return True
        else:
            return False
    
    def is_valid_visa_number(self, number):
        # Luhn's algorithm to validate the Visa number
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10 == 0
    
    def validate_date(self, input_text):
        pattern = r'^\d{2}/\d{2}$'  # Regular expression for mm/yy format
    
        if re.match(pattern, input_text):
            return True
        else:
            return False

    def validate_cvv(self, input_text):
        pattern = r'^\d{3}$'  # Regular expression for mm/yy format
    
        if re.match(pattern, input_text):
            return True
        else:
            return False
    
    def confirm_payment(self):
        if self.visa:
            if not self.validate_payment():
                messagebox.showerror("Payment", "Invalid Visa Number.")
                return
            if not self.validate_date(self.entry_expiry_date.get()):
                messagebox.showerror("Payment", "Invalid Expiry Date.")
                return
            if not self.validate_cvv(self.entry_cvv.get()):
                messagebox.showerror("Payment", "Invalid CVV Number.")
                return
        
        payment_method = self.payment_method_var.get()
        promo_code = self.entry_promo_code.get()

        if not payment_method:
            messagebox.showerror("Payment", "Payment Method is empty")
            return

        if not promo_code:
            messagebox.showerror("Payment", "Promo Code is empty")
            return
        
        with self.db_conn:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT payment_id FROM payments ORDER BY payment_id DESC LIMIT 1")
            result = cursor.fetchone()
            payment_id = int(result[0]) + 1
            cursor.execute("""
                        INSERT INTO payments (payment_id, cart_id, total_price, payment_method, payment_date)
                        VALUES (?, ?, ?, ?, datetime('now'))
                    """, (payment_id, self.cart_id, self.total_price, payment_method))
            cursor.execute("""
                        INSERT INTO payment_promocode (payment_id, code)
                        VALUES (?, ?)
                    """, (payment_id, promo_code))

        messagebox.showinfo("Success", "Payment processed successfully.")
        #self.switch_to_home_callback()

