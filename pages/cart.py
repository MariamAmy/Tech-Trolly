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

    def fetch_N_cart_items(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT COUNT(i.name) \
                       FROM items AS i \
                       JOIN cart_item AS ci \
                       ON i.item_id = ci.item_id \
                       WHERE ci.cart_id = ?", (self.cart_id,))
        self.N_cart_items = cursor.fetchone()[0]
        self.button_cart.configure(text=self.N_cart_items)

    def fetch_and_display_cart_items(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT i.item_id, i.name, i.price, ci.quantity \
                       FROM items AS i \
                       JOIN cart_item AS ci \
                       ON i.item_id = ci.item_id \
                       WHERE ci.cart_id = ?", (self.cart_id,))
        self.cart_items = cursor.fetchall()
            
    def update_item_frames(self):
        # Clear out any existing item frames
        for frame in self.item_frames:
            for i in frame:
                i.destroy()
        
        self.item_frames.clear()
        # Fetch the latest cart items from the database
        self.fetch_and_display_cart_items()

        # Create a frame for each cart item
        for i, (item_id, name, price, quantity) in enumerate(self.cart_items, start=0):
            lbl_item_name = tk.Label(self.center_frame, text=name)
            lbl_item_name.grid(row=i, column=0, padx=5, pady=5, sticky='w')

            lbl_price = tk.Label(self.center_frame, text=f"${price:.2f}")
            lbl_price.grid(row=i, column=1, padx=5, pady=5, sticky='w')

            btn_minus = tk.Button(self.center_frame, text="-", 
                                  command=lambda item_id = item_id: self.update_quantity(item_id, name, -1))
            btn_minus.grid(row=i, column=2, padx=5, pady=5, sticky='w')
            lbl_quantity = tk.Label(self.center_frame, text=str(quantity))
            lbl_quantity.grid(row=i, column=3, padx=5, pady=5, sticky='w')
            btn_plus = tk.Button(self.center_frame, text="+", 
                                 command=lambda item_id = item_id: self.update_quantity(item_id, name, 1))
            btn_plus.grid(row=i, column=4, padx=5, pady=5, sticky='w')

            lbl_total = tk.Label(self.center_frame, text=f"${price * quantity:.2f}")
            lbl_total.grid(row=i, column=5, padx=5, pady=5, sticky='e')
            self.item_frames.append([lbl_item_name, lbl_price, btn_minus, lbl_quantity, btn_plus, lbl_total])
        
        # Total price label
        self.total_frame = tk.Frame(self.center_frame)
        self.total_frame.grid(row=len(self.cart_items) + 1, column=0, columnspan=6, pady=20, sticky='ew')

        self.total_frame.grid_columnconfigure(0, weight=1)
        self.total_frame.grid_columnconfigure(1, weight=1)
        self.total_frame.grid_columnconfigure(2, weight=1)
        self.total_frame.grid_columnconfigure(3, weight=1)
        self.total_frame.grid_columnconfigure(4, weight=1)
        self.total_frame.grid_columnconfigure(5, weight=1)

        self.lbl_cart_total_text = tk.Label(self.total_frame, text="Cart Total:")
        self.lbl_cart_total_text.grid(row=0, column=0, sticky='w')

        self.lbl_cart_total = tk.Label(self.total_frame, text=f"${self.calculate_total():.2f}")
        self.lbl_cart_total.grid(row=0, column=5, sticky='e')
            
    def update_quantity(self, item_id, name, change):
        cursor = self.db_conn.cursor()
        if change == -1:
            cursor.execute("UPDATE cart_item SET quantity = quantity - 1 WHERE cart_id = ? AND item_id = ?", (self.cart_id, item_id))
        else:
            cursor.execute("UPDATE cart_item SET quantity = quantity + 1 WHERE cart_id = ? AND item_id = ?", (self.cart_id, item_id))

        cursor.execute("SELECT quantity FROM cart_item WHERE cart_id = ? AND item_id = ?", (self.cart_id, item_id))
        self.lbl_cart_total.configure(text=f"${self.calculate_total():.2f}")
        new_quantity = cursor.fetchone()[0]
        
        if new_quantity <= 0:
            cursor.execute("DELETE FROM cart_item WHERE cart_id = ? AND item_id = ?", (self.cart_id, item_id))
            messagebox.showinfo("Item removed", f"Item {name} has been removed from your cart.")

        self.db_conn.commit()
        self.N_cart_items = self.fetch_N_cart_items()
        self.button_cart.configure(text=self.N_cart_items)
        self.total_frame.destroy()
        self.update_item_frames()

    def calculate_total(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT SUM(i.price * ci.quantity) \
                       FROM items AS i \
                       JOIN cart_item AS ci \
                       ON i.item_id = ci.item_id \
                       WHERE ci.cart_id = ?", (self.cart_id,))
        total = cursor.fetchone()[0]
        return total if total else 0.0

    def proceed_to_payment(self):
        # Placeholder function for proceeding to payment
        messagebox.showinfo("Proceed to Payment", "Now proceeding to the payment page.")
