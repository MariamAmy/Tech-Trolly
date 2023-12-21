import tkinter as tk
from tkinter import messagebox, font
from datetime import datetime

class AdminPage(tk.Frame):
    """
    Represents the admin page of the Tech Trolley application.

    Attributes:
    - master: The master widget.
    - switch_to_home_callback: Callback function to switch to the home page.
    - switch_to_signup_callback: Callback function to switch to the signup page.
    - db_conn: SQLite database connection.
    """

    def __init__(self, master, switch_to_home_callback, switch_to_signup_callback, db_conn):
        """
        Initialize the AdminPage.

        Parameters:
        - master: The master widget.
        - switch_to_home_callback: Callback function to switch to the home page.
        - switch_to_signup_callback: Callback function to switch to the signup page.
        - db_conn: SQLite database connection.
        """

        super().__init__(master)
        self.db_conn = db_conn
        self.switch_to_home_callback = switch_to_home_callback
        self.switch_to_signup_callback = switch_to_signup_callback

        # Set up grid configuration for the frames
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.configure(bg='#d9f4ff')
        self.create_widgets()

    def create_widgets(self):
        """
        Create and configure the widgets for the admin page.
        """

        # Define the font styles
        button_font = font.Font(family="Arial", size=12, weight="bold")

        self.top_left_frame = tk.Frame(self, bg='#d9f4ff')
        self.top_left_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.button_home = tk.Button(self.top_left_frame, text="Home", command=self.switch_to_home_callback, font=button_font)
        self.button_home.pack(side="left", padx=5, pady=5)

        # Add admin button and frame
        self.add_frame = tk.Frame(self, bg='#d9f4ff')
        self.add_frame.grid(row=0, column=2, sticky="ne", padx=10, pady=10)
        self.button_add = tk.Button(self.add_frame, text="Add admin", command=self.switch_to_signup_callback, font=button_font)
        self.button_add.pack(side="right", padx=5, pady=5)

        # Center frame for form entries
        self.center_frame = tk.Frame(self, bg='#ffffff', bd=2, relief='groove')
        self.center_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

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
        self.label_tech_trolley = tk.Label(self.center_frame, text="Tech Trolley", font=title_font, bg='#ffffff')
        self.label_tech_trolley.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Labels and entry widgets for item details
        self.item_name = tk.Label(self.center_frame, text="Item Name:", font=label_font, bg='#ffffff')
        self.item_name.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.item_name_entry = tk.Entry(self.center_frame, font=entry_font, width=25, bg='#f8f8f8')
        self.item_name_entry.grid(row=1, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky='ew')

        self.brand_name = tk.Label(self.center_frame, text="Brand Name:", font=label_font, bg='#ffffff')
        self.brand_name.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.brand_name_entry = tk.Entry(self.center_frame, font=entry_font, width=25, bg='#f8f8f8')
        self.brand_name_entry.grid(row=2, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky='ew')
        self.brand_name_entry.bind("<FocusOut>", self.brand_name_focus_out)

        self.brand_nationality = tk.Label(self.center_frame, text="Brand Nationality:", font=label_font, bg='#ffffff')
        self.brand_nationality.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.brand_nationality_entry = tk.Entry(self.center_frame, font=entry_font, width=25, bg='#f8f8f8')
        self.brand_nationality_entry.grid(row=3, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky='ew')

        self.price = tk.Label(self.center_frame, text="Price:", font=label_font, bg='#ffffff')
        self.price.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.price_entry = tk.Entry(self.center_frame, font=entry_font, width=25, bg='#f8f8f8')
        self.price_entry.grid(row=4, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky='ew')

        self.quantity = tk.Label(self.center_frame, text="Quantity:", font=label_font, bg='#ffffff')
        self.quantity.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.quantity_entry = tk.Entry(self.center_frame, font=entry_font, width=25, bg='#f8f8f8')
        self.quantity_entry.grid(row=5, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky='ew')

        self.expiry_date = tk.Label(self.center_frame, text="Expiry Date:", font=label_font, bg='#ffffff')
        self.expiry_date.grid(row=6, column=0, padx=20, pady=10, sticky="w")
        self.expiry_date_entry = tk.Entry(self.center_frame, font=entry_font, width=25, bg='#f8f8f8')
        self.expiry_date_entry.grid(row=6, column=1, padx=20, pady=10, ipadx=5, ipady=5, sticky='ew')

        # Add item button
        self.add_item_button = tk.Button(self.center_frame, text="Add Item", font=button_font, command=self.add_item)
        self.add_item_button.grid(row=7, column=0, columnspan=2, padx=20, pady=10)

        # Hide brand nationality initially
        self.brand_nationality.grid_remove()
        self.brand_nationality_entry.grid_remove()

    def brand_name_focus_out(self, event):
        """
        Handle the focus out event for the brand name entry.
        If the brand name exists, hide the brand nationality entry; otherwise, show it.
        """

        brand_name = self.brand_name_entry.get()
        cursor = self.db_conn.cursor()

        # Fetch existing brand names from the database
        cursor.execute("SELECT name FROM brands")
        brands = [i[0] for i in cursor.fetchall()]

        # Check if the entered brand name exists
        if brand_name in brands:
            self.brand_nationality.grid_remove()
            self.brand_nationality_entry.grid_remove()
        else:
            self.brand_nationality.grid()
            self.brand_nationality_entry.grid()

    def add_item(self):
        """
        Handle the add item button click event.
        Add a new item to the database.
        """
        
        # Fetch input values from the entry widgets
        item_name = self.item_name_entry.get()
        brand_name = self.brand_name_entry.get()
        brand_nationality = self.brand_nationality_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        expiry_date = self.expiry_date_entry.get()

        # Check for empty fields
        if not item_name or not brand_name or not price or not quantity or not expiry_date:
            messagebox.showerror("Add Item", "Please fill in all fields")
            return
        
        # Validate price and quantity as positive numbers
        try:
            price = float(price)
            quantity = int(quantity)
            if price <= 0 or quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Add Item", "Price and quantity must be positive numbers")
            return
        
        # Validate expiry date format
        try:
            datetime.strptime(expiry_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Add Item", "Invalid expiry date format. Use YYYY-MM-DD.")
            return

        cursor = self.db_conn.cursor()

        # Check if brand nationality is provided
        if brand_nationality:
            # Generate a new brand ID
            cursor.execute("SELECT brand_id FROM brands ORDER BY brand_id DESC LIMIT 1")
            result = cursor.fetchone()
            new_brand_id = int(result[0]) + 1
            # Insert new brand into the database
            cursor.execute("INSERT INTO brands (brand_id, name, nationality) VALUES (?, ?, ?)",
                           (new_brand_id, brand_name, brand_nationality))
            self.db_conn.commit()

        # Fetch existing item names and brand IDs from the database
        cursor.execute("SELECT name FROM items")
        items_names = [i[0] for i in cursor.fetchall()]

        cursor.execute("SELECT b.name FROM items AS i JOIN brands AS b ON i.brand_id = b.brand_id WHERE i.name = ?", (item_name,))
        brands = [i[0] for i in cursor.fetchall()]

        cursor.execute("SELECT brand_id FROM brands WHERE name = ?", (brand_name,))
        brand_id = cursor.fetchone()[0]

        # Check if the item already exists, update if it does, otherwise, insert a new item
        if item_name in items_names and brand_name in brands:
            cursor.execute("SELECT item_id FROM items WHERE name = ? AND brand_id = ?", (item_name, brand_id))
            item_id = cursor.fetchone()[0]
            cursor.execute("UPDATE items SET price = ?, quantity = ?, expiry_date = ? WHERE item_id = ? AND brand_id = ?",
                           (price, quantity, expiry_date, item_id, brand_id))
            self.db_conn.commit()
            messagebox.showinfo("Success", "Item added successfully")
        else:
            cursor.execute("SELECT item_id FROM items ORDER BY item_id DESC LIMIT 1")
            result = cursor.fetchone()
            item_id = int(result[0]) + 1
            cursor.execute("INSERT INTO items (item_id, name, brand_id, price, quantity, expiry_date) VALUES (?, ?, ?, ?, ?, ?)", 
                           (item_id, item_name, brand_id, price, quantity, expiry_date))
            self.db_conn.commit()
            messagebox.showinfo("Success", "Item added successfully")