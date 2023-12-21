import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, font
import re 

class PaymentPage(tk.Frame):
    """
    Represents the payment page of the Tech Trolley application.

    Attributes:
    - master: The master widget.
    - switch_to_cart_callback: Callback function to switch to the cart page.
    - switch_to_home_callback: Callback function to switch to the home page.
    - db_conn: SQLite database connection.
    - cart_id: ID of the current shopping cart.
    - total_price: Total price of items in the cart.
    - num_cart_items: Number of items in the cart.
    """

    def __init__(self, master, switch_to_cart_callback, switch_to_home_callback, db_conn, cart_id, total_price, num_cart_items):
        """
        Initialize the PaymentPage.

        Parameters:
        - master: The master widget.
        - switch_to_cart_callback: Callback function to switch to the cart page.
        - switch_to_home_callback: Callback function to switch to the home page.
        - db_conn: SQLite database connection.
        - cart_id: ID of the current shopping cart.
        - total_price: Total price of items in the cart.
        - num_cart_items: Number of items in the cart.
        """

        super().__init__(master)
        self.switch_to_cart_callback = switch_to_cart_callback
        self.switch_to_home_callback = switch_to_home_callback
        self.db_conn = db_conn
        self.cart_id = cart_id
        self.total_price = total_price if total_price else 0
        self.num_cart_items = num_cart_items
        self.visa = 0
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.applied_promocodes = []
        self.configure(bg="#d9f4ff")
        self.create_widgets()

    def create_widgets(self):
        """
        Create and configure the widgets for the payment page.
        """
        
        # Define the font styles
        button_font = font.Font(family="Arial", size=12, weight="bold")

        self.top_left_frame = tk.Frame(self, bg="#d9f4ff")
        self.top_left_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.button_home = tk.Button(self.top_left_frame, text="Home", command=self.switch_to_home_callback, font=button_font)
        self.button_home.pack(side="left", padx=5, pady=5)

        # Load the image for the cart button and resize it
        self.original_cart_image = tk.PhotoImage(file="cart.png") 
        self.cart_image = self.original_cart_image.subsample(5, 5) 

        self.top_right_frame = tk.Frame(self, bg="#d9f4ff")
        self.top_right_frame.grid(row=0, column=2, sticky="ne", padx=10, pady=10)

        # Create the cart button and place it in the top_right_frame
        self.button_cart = tk.Button(self.top_right_frame, image=self.cart_image, compound="bottom", text=self.num_cart_items,
                                     font=button_font, command=self.switch_to_cart_callback)
        self.button_cart.pack(side="right", padx=5, pady=5)

        # Center frame for the other widgets with a white background
        self.center_frame = tk.Frame(self, bg="#ffffff" , padx = 10, pady = 20)
        self.center_frame.grid(row=1, column=1, sticky="nsew", padx=50, pady=50)
        self.create_center_widgets()

    def create_center_widgets(self):
        """
        Create and configure the widgets for the center frame of the payment page.
        """

        # Define the font styles
        title_font = font.Font(family="Arial", size=24, weight="bold")
        label_font = font.Font(family="Arial", size=14)
        entry_font = font.Font(family="Arial", size=12)
        button_font = font.Font(family="Arial", size=12, weight="bold")

        # Market name label
        self.label_tech_trolley = tk.Label(self.center_frame, text="Tech Trolley", font=title_font, bg="#ffffff")
        self.label_tech_trolley.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10, 20))

        # Widgets for entering promo code
        self.label_promo_code = tk.Label(self.center_frame, text="Promo code", font=label_font, bg="#ffffff")
        self.label_promo_code.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.entry_promo_code = tk.Entry(self.center_frame, font=entry_font, bg="#f8f8f8")
        self.entry_promo_code.grid(row=1, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky="w")
        self.apply_promo_code_button = tk.Button(self.center_frame, text="Apply promocode", command=self.apply_promo_code, 
                                                 font=button_font)
        self.apply_promo_code_button.grid(row=1, column=2, pady=5, sticky="e")

        # Widgets for selecting payment method
        self.label_payment_method = tk.Label(self.center_frame, text="Payment method", font=label_font, bg="#ffffff")
        self.label_payment_method.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.payment_method_var = tk.StringVar()
        self.payment_method_options = ["Credit Card", "Debit Card", "Cash on Delivery"]
        self.optionmenu_payment_method = ttk.Combobox(self.center_frame, textvariable=self.payment_method_var, font=entry_font,
                                                      values=self.payment_method_options, width=18)
        self.optionmenu_payment_method.grid(row=2, column=1, columnspan=2, padx=20, pady=10, sticky="ew")
        self.optionmenu_payment_method.bind("<<ComboboxSelected>>", self.on_payment_method_changed)

        # Widgets for entering Visa details
        self.label_visa = tk.Label(self.center_frame, text="Visa Number", font=label_font, bg="#ffffff")
        self.label_visa.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.entry_visa_number = tk.Entry(self.center_frame, font=entry_font, width=25, bg="#f8f8f8")
        self.entry_visa_number.grid(row=3, column=1, columnspan=2, padx=20, pady=10, ipadx=5, ipady=5, sticky="ew")

        # Widgets for entering expiry date
        self.label_expiry_date = tk.Label(self.center_frame, text="Expiry Date (MM/YY)", font=label_font, bg="#ffffff")
        self.label_expiry_date.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.entry_expiry_date = tk.Entry(self.center_frame, font=entry_font, width=25, bg="#f8f8f8")
        self.entry_expiry_date.grid(row=4, column=1, columnspan=2, padx=20, pady=10, ipadx=5, ipady=5, sticky="ew")

        # Widgets for entering CVV
        self.label_cvv = tk.Label(self.center_frame, text="CVV", font=label_font, bg="#ffffff")
        self.label_cvv.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.entry_cvv = tk.Entry(self.center_frame, show="*", font=entry_font, width=25, bg="#f8f8f8")
        self.entry_cvv.grid(row=5, column=1, columnspan=2, padx=20, pady=10, ipadx=5, ipady=5, sticky="ew")

        # Hide Visa details initially
        self.label_visa.grid_remove()
        self.entry_visa_number.grid_remove()
        self.label_expiry_date.grid_remove()
        self.entry_expiry_date.grid_remove()
        self.label_cvv.grid_remove()
        self.entry_cvv.grid_remove()

        # Widgets for entering address
        self.label_address = tk.Label(self.center_frame, text="Address", font=label_font, bg="#ffffff")
        self.label_address.grid(row=6, column=0, padx=20, pady=10, sticky="w")
        self.entry_address = tk.Entry(self.center_frame, font=entry_font, width=25, bg="#f8f8f8")
        self.entry_address.grid(row=6, column=1, columnspan=2, padx=20, pady=10, ipadx=5, ipady=5, sticky="ew")

        # Widgets for total price
        self.total_price_label = tk.Label(self.center_frame, text=f"Total price: ${round(self.total_price, 2)}", 
                                          font=label_font, bg="#ffffff")
        self.total_price_label.grid(row=7, column=0, columnspan=3, pady=20, sticky="ew")

        # Button to confirm payment
        self.button_payment = tk.Button(self.center_frame, text="Confirm Payemnt", command=self.confirm_payment, font=button_font)
        self.button_payment.grid(row=8, column=0, columnspan=3, pady=20)

    def on_payment_method_changed(self, event=None):
        """
        Handle the event when the payment method is changed in the Combobox.
        """

        payment_method = self.payment_method_var.get()
        if payment_method in ["Credit Card", "Debit Card"]:
            # Show Visa details if Credit Card or Debit Card is selected
            self.label_visa.grid()
            self.entry_visa_number.grid()
            self.label_expiry_date.grid()
            self.entry_expiry_date.grid()
            self.label_cvv.grid()
            self.entry_cvv.grid()
            self.visa = 1
        else:
            # Hide Visa details for other payment methods
            self.label_visa.grid_remove()
            self.entry_visa_number.grid_remove()
            self.label_expiry_date.grid_remove()
            self.entry_expiry_date.grid_remove()
            self.label_cvv.grid_remove()
            self.entry_cvv.grid_remove()
            self.visa = 0

    def apply_promo_code(self):
        """
        Apply promocode discount if it is valid.
        """

        promo_code = self.entry_promo_code.get()
        if not self.is_valid_promo_code(promo_code):
            messagebox.showerror("Payment", "Invalid Promo Code.")
            return
        self.applied_promocodes.append(promo_code)
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT discount_amount FROM promocodes WHERE code = ?", (promo_code,))
        discount = cursor.fetchone()[0]
        new_price = self.total_price * (1 - (discount / 100))
        self.total_price = new_price
        self.total_price_label.configure(text=f"Total price: ${round(new_price, 2)}")
        messagebox.showinfo("Payment", "Promocode Applied.")

    def is_valid_promo_code(self, code):
        """
        Check if the given promo code is valid.

        Parameters:
        - code: The promo code to be checked.

        Returns:
        - bool: True if the promo code is valid, False otherwise.
        """
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM promocodes WHERE code = ?", (code,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

    def validate_payment(self):
        """
        Validate the entered Visa number.

        Returns:
        - bool: True if the Visa number is valid, False otherwise.
        """

        visa_number = self.entry_visa_number.get()
        if self.is_valid_visa_number(visa_number):
            return True
        else:
            return False

    def is_valid_visa_number(self, number):
        """
        Check if the given Visa number is valid.

        Parameters:
        - number: The Visa number to be checked.

        Returns:
        - bool: True if the Visa number is valid, False otherwise.
        """

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
        """
        Validate the entered date.

        Parameters:
        - input_text: The date string to be validated.

        Returns:
        - bool: True if the date is valid, False otherwise.
        """

        pattern = r"^\d{2}/\d{2}$"

        if re.match(pattern, input_text):
            return True
        else:
            return False

    def validate_cvv(self, input_text):
        """
        Validate the entered CVV number.

        Parameters:
        - input_text: The CVV number to be validated.

        Returns:
        - bool: True if the CVV number is valid, False otherwise.
        """

        pattern = r"^\d{3}$"

        if re.match(pattern, input_text):
            return True
        else:
            return False

    def confirm_payment(self):
        """
        Handle the event when the payment is confirmed.
        """

        # Validation for Visa details if Credit Card or Debit Card is selected
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

        # Get selected payment method and promo code
        payment_method = self.payment_method_var.get()
        address = self.entry_address.get()

        # Check for empty payment method
        if not payment_method or not address:
            messagebox.showerror("Payment", "Please fill in all fields")
            return

        # Insert payment details into the database
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT payment_id FROM payments ORDER BY payment_id DESC LIMIT 1")
        result = cursor.fetchone()
        payment_id = int(result[0]) + 1
        for i in self.applied_promocodes:
            cursor.execute("INSERT INTO payment_promocode (payment_id, code) VALUES (?, ?)", (payment_id, i))
        cursor.execute("INSERT INTO payments (payment_id, cart_id, total_price, payment_method, payment_date) \
                        VALUES (?, ?, ?, ?, datetime('now'))",
                       (payment_id, self.cart_id, round(self.total_price, 2), payment_method))
        self.db_conn.commit()

        # Show success message and switch to the home page
        messagebox.showinfo("Payment", "Payment processed successfully.")
        self.switch_to_home_callback()

