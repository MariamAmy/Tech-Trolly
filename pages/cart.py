import tkinter as tk
from tkinter import messagebox

class CartPage(tk.Frame):
    def __init__(self, master, switch_to_payment_callback, db_conn, cart_id):
        super().__init__(master)
        self.db_conn = db_conn
        self.cart_id= cart_id
        self.switch_to_payment_callback = switch_to_payment_callback
        
        # Configure grid for center alignment
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_forget()

        self.create_widgets()
        self.fetch_and_display_cart_items()
        self.N_cart_items = self.fetch_N_cart_items()

    def create_widgets(self):
        # Home button frame
        self.home_frame = tk.Frame(self)
        self.home_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        self.button_home = tk.Button(self.home_frame, text="Home")  # Add command as needed
        self.button_home.pack(side="left", padx=5, pady=5)

        # Cart button frame
        self.cart_frame = tk.Frame(self)
        self.cart_frame.grid(row=0, column=2, sticky="ne", padx=10, pady=10)
        self.button_cart = tk.Button(self.cart_frame, compound = "bottom",
                                    command=self.on_cart_click)
        self.button_cart.pack(side="right", padx=5, pady=5)

        # Center frame
        self.center_frame = tk.Frame(self)
        self.center_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        self.item_frames = []

        # Function to update the item frames
        self.update_item_frames()

        # Proceed to payment button
        self.btn_proceed = tk.Button(self, text="Proceed to Payment", command=self.switch_to_payment_callback)
        self.btn_proceed.grid(row=2, column=1, sticky="s")

    def on_cart_click(self):
        pass

    