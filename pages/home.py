import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta

class Item:
    """Class representing an item in the shop."""
    def __init__(self, item_id, name, brand_name, brand_nationality, price, sold, sold_24h, quantity, discount=False):
        self.item_id = item_id
        self.name = name
        self.brand_name = brand_name
        self.brand_nationality = brand_nationality
        self.price = price
        self.sold = sold
        self.sold_24h = sold_24h
        self.discount = discount
        self.quantity = 0
        self.quantity_in_store = quantity

class ItemFrame(tk.Frame):
    """A frame representing an item with controls to change quantity and add to cart."""
    def __init__(self, master, item, add_to_cart, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.item = item
        self.add_to_cart = add_to_cart

        # Create the GUI elements
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=self.item.name).grid(row=0, column=0, sticky="w")
        tk.Label(self, text=self.item.brand_name).grid(row=0, column=1, sticky="w")
        tk.Label(self, text=f"${self.item.price:.2f}").grid(row=0, column=2, sticky="w")
        if self.item.discount:
            tk.Label(self, text="Discount!", fg='red').grid(row=0, column=3, sticky="w")
        tk.Label(self, text=f"Sold: {self.item.sold}").grid(row=1, column=0, columnspan=2, sticky="w")
        tk.Label(self, text=f"Sold in 24h: {self.item.sold_24h}").grid(row=1, column=2, columnspan=2, sticky="w")

        self.quantity_label = tk.Label(self, text=f"Quantity: {self.item.quantity}")
        self.quantity_label.grid(row=2, column=0, sticky="w")

        # Plus and minus buttons to adjust quantity
        self.minus_button = tk.Button(self, text="-", command=self.decrease_quantity)
        self.minus_button.grid(row=2, column=1)
        self.plus_button = tk.Button(self, text="+", command=self.increase_quantity)
        self.plus_button.grid(row=2, column=2)

        self.add_button = tk.Button(self, text="Add to Cart", command=lambda item = self.item: self.add_to_cart(item))
        self.add_button.grid(row=2, column=3)

    def increase_quantity(self):
        self.item.quantity += 1
        self.quantity_label.config(text=f"Quantity: {self.item.quantity}")

    def decrease_quantity(self):
        if self.item.quantity > 0:
            self.item.quantity -= 1
            self.quantity_label.config(text=f"Quantity: {self.item.quantity}")

class HomePage(tk.Frame):
    def __init__(self, master, switch_to_cart_callback, switch_to_admin_callback, admin,
                 db_conn, customer_email, cart_id=None):
        super().__init__(master)
        self.switch_to_cart_callback = switch_to_cart_callback
        self.switch_to_admin_callback = switch_to_admin_callback
        self.db_conn = db_conn
        self.cart_id = cart_id
        self.customer_email = customer_email

        # Configure grid for center alignment
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_forget()

        self.home_frame = tk.Frame(self)
        self.home_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        self.button_home = tk.Button(self.home_frame, text="Home")
        self.button_home.pack(side="left", padx=5, pady=5)
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT admin FROM customers WHERE email=?", (self.customer_email,))
        self.admin = cursor.fetchone()[0]

        self.button_admin = tk.Button(self, text="Admin Page", command=self.switch_to_admin_callback)
        if self.admin:
            self.button_admin.grid(row=0, column=1, sticky="n", padx=10, pady=10)
        else:
            self.button_admin.grid_remove()

        # Load the image for the cart button and resize it
        self.original_cart_image = tk.PhotoImage(file="cart.png") 
        self.cart_image = self.original_cart_image.subsample(5, 5)

        # Cart button frame
        self.cart_frame = tk.Frame(self)
        self.cart_frame.grid(row=0, column=2, sticky="ne", padx=10, pady=10)
        self.button_cart = tk.Button(self.cart_frame, image=self.cart_image, compound = "bottom",
                                    command=self.switch_to_cart_callback)
        self.button_cart.pack(side="right", padx=5, pady=5)

        self.center_frame = tk.Frame(self)
        self.center_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)
        self.center_frame.grid_columnconfigure(0, weight=1)
        self.center_frame.grid_columnconfigure(1, weight=1)
        self.center_frame.grid_columnconfigure(2, weight=1)

        self.search_var = tk.StringVar()
        self.search_bar = tk.Entry(self.center_frame, textvariable=self.search_var)
        self.search_bar.grid(row=0, column=0, columnspan=3, sticky='ew', padx=10, pady=10)

        self.items_frame = tk.Frame(self.center_frame)
        self.items_frame.grid(row=1, column=2, columnspan=2)
        
        # Create a list to keep track of the item frames
        self.item_frames = []
        self.shop_items = []

        self.fetch_and_display_items()

        self.display_items()

        self.add_to_cart_button_visibilty()

        # Filter frame
        self.filter_frame = tk.Frame(self.center_frame)
        self.filter_frame.grid(row=1, column=0, sticky="nws", padx=10, pady=10)

        # Brand Name Filter
        self.brand_name_var = tk.StringVar()
        self.brand_name_combo = ttk.Combobox(self.filter_frame, textvariable=self.brand_name_var)
        self.brand_name_combo['values'] = ['Brand A', 'Brand B']  # Add more brands as needed
        self.brand_name_combo.grid(row=0, column=0, padx=5, pady=5)
        self.brand_name_combo.set("Select Brand")

        # Brand Nationality Filter
        self.brand_nationality_var = tk.StringVar()
        self.brand_nationality_combo = ttk.Combobox(self.filter_frame, textvariable=self.brand_nationality_var)
        self.brand_nationality_combo['values'] = ['USA', 'Germany']  # Add more nationalities as needed
        self.brand_nationality_combo.grid(row=1, column=0, padx=5, pady=5)
        self.brand_nationality_combo.set("Select Nationality")

        # Price Range Filter
        self.min_price_label = tk.Label(self.filter_frame, text="Min Price")
        self.min_price_label.grid(row=2, column=0, padx=5, pady=2)
        self.min_price = tk.Scale(self.filter_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_max_price)
        self.min_price.grid(row=3, column=0, padx=5, pady=5)

        # Price Range Filter - Maximum Price
        self.max_price_label = tk.Label(self.filter_frame, text="Max Price")
        self.max_price_label.grid(row=4, column=0, padx=5, pady=2)
        self.max_price = tk.Scale(self.filter_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_min_price)
        self.max_price.grid(row=5, column=0, padx=5, pady=5)

        # Set default values
        self.min_price.set(20)  # Set to your default minimum
        self.max_price.set(80)

        # Update items_frame grid
        self.items_frame.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=20, pady=20)


    def update_min_price(self, val):
        min_val = self.min_price.get()
        max_val = int(val)
        if max_val < min_val:
            self.min_price.set(max_val)

    def update_max_price(self, val):
        max_val = self.max_price.get()
        min_val = int(val)
        if min_val > max_val:
            self.max_price.set(min_val)

    
    def display_items(self):
        for i, item in enumerate(self.shop_items):
            row = i // 3
            column = i % 3
            frame = ItemFrame(self.items_frame, item, self.add_to_cart)
            frame.grid(row=row, column=column, padx=10, pady=5, sticky='ew')  # Adjust row and column as needed
            self.item_frames.append(frame)
            

    def fetch_and_display_items(self):
        current_time = datetime.now()
        one_day_ago = current_time - timedelta(days=1)
        cursor = self.db_conn.cursor()

        # Get items and brand info from the database
        cursor.execute('''
            SELECT i.item_id, i.name, i.quantity, i.price, i.expiry_date, b.name, b.nationality, b.brand_id,
            (SELECT COUNT(*) FROM cart_item WHERE item_id = i.item_id) AS sold,
            (SELECT COUNT(*) FROM cart_item AS ci JOIN payments AS p ON ci.cart_id = p.cart_id WHERE p.payment_date >= ?) AS sold_24h,
            (SELECT discount_amount FROM discounts WHERE item_id = i.item_id AND start_date <= ? AND end_date >= ?) AS discount
            FROM items i
            JOIN brands b ON i.brand_id = b.brand_id
            ''', (one_day_ago, current_time, current_time))

        for row in cursor.fetchall():
            item_id, item_name, item_quantity, item_price, expiry_date, brand_name, \
            brand_nationality, brand_id, sold, sold_24h, discount = row
            if discount:
                discount_price = item_price * (1 - (discount / 100))
            else:
                discount_price = item_price
            # Create and display the item frame
            item = Item(item_id, item_name, brand_name, brand_nationality, discount_price, sold, sold_24h, 
                        item_quantity, discount=bool(discount))
            self.shop_items.append(item)
    
    def add_to_cart(self, item):
        cursor = self.db_conn.cursor()
        if not self.cart_id:
            cursor.execute("SELECT cart_id FROM shopping_carts ORDER BY cart_id DESC LIMIT 1")
            result = cursor.fetchone()
            self.cart_id = int(result[0]) + 1
            # Create a new cart
            cursor.execute('INSERT INTO shopping_carts (cart_id, customer_email, creation_time) VALUES (?, ?, ?)', 
                                (self.cart_id, self.customer_email, datetime.now()))
            self.db_conn.commit()
        
        # Add the item to the cart
        cursor.execute('INSERT INTO cart_item (cart_id, item_id, quantity) VALUES (?, ?, ?)', (self.cart_id, item.item_id, item.quantity))
        self.db_conn.commit()
        self.add_to_cart_button_visibilty()
        messagebox.showinfo("Cart", f"Added {item.quantity} of {item.name} to the cart.")

    def add_to_cart_button_visibilty(self):
        if self.cart_id:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT item_id FROM cart_item WHERE cart_id = ?", (self.cart_id,))
            items = cursor.fetchall()
            for n, i in enumerate(items):
                items[n] = i[0]
            for i in self.item_frames:
                if i.item.item_id in items:
                    i.quantity_label.grid_forget()
                    i.minus_button.grid_forget()
                    i.plus_button.grid_forget()
                    i.add_button.grid_forget()