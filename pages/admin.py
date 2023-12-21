import tkinter as tk
from tkinter import messagebox

class AdminPage(tk.Frame):
    def __init__(self, master, db_conn):
        super().__init__(master)
        self.db_conn = db_conn
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_forget()
        self.create_widgets()

    def create_widgets(self):
        self.home_frame = tk.Frame(self)
        self.home_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        self.button_home = tk.Button(self.home_frame, text="Home")  # Add command as needed
        self.button_home.pack(side="left", padx=5, pady=5)

        # Center frame
        self.center_frame = tk.Frame(self)
        self.center_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        # Create and place labels and entry widgets for each attribute of an item
        self.item_name = tk.Label(self.center_frame, text="Item Name:")
        self.item_name.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.item_name_entry = tk.Entry(self.center_frame)
        self.item_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.brand_name = tk.Label(self.center_frame, text="Brand Name:")
        self.brand_name.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.brand_name_entry = tk.Entry(self.center_frame)
        self.brand_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.brand_name_entry.bind("<FocusOut>", self.brand_name_focus_out)

        self.brand_nationality = tk.Label(self.center_frame, text="Brand Nationality:")
        self.brand_nationality.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.brand_nationality_entry = tk.Entry(self.center_frame)
        self.brand_nationality_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        self.price = tk.Label(self.center_frame, text="Price:")
        self.price.grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.price_entry = tk.Entry(self.center_frame)
        self.price_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        self.quantity = tk.Label(self.center_frame, text="Quantity:")
        self.quantity.grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.quantity_entry = tk.Entry(self.center_frame)
        self.quantity_entry.grid(row=4, column=1, padx=10, pady=5, sticky='w')

        self.expiry_date = tk.Label(self.center_frame, text="Expiry Date:")
        self.expiry_date.grid(row=5, column=0, padx=10, pady=5, sticky='w')
        self.expiry_date_entry = tk.Entry(self.center_frame)
        self.expiry_date_entry.grid(row=5, column=1, padx=10, pady=5, sticky='w')

        # Create a button to add the item to the database
        self.add_item_button = tk.Button(self.center_frame, text="Add Item", command=self.add_item)
        self.add_item_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.brand_nationality.grid_remove()
        self.brand_nationality_entry.grid_remove()

    def brand_name_focus_out(self, event):
        brand_name = self.brand_name_entry.get()
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT name FROM brands")
        brands = cursor.fetchall()
        for n, i in enumerate(brands):
            brands[n] = i[0]
        if brand_name in brands:
            self.brand_nationality.grid_remove()
            self.brand_nationality_entry.grid_remove()
        else:
            self.brand_nationality.grid()
            self.brand_nationality_entry.grid()
        
        
    def add_item(self):
        # Retrieve data from entries
        item_name = self.item_name_entry.get()
        brand_name = self.brand_name_entry.get()
        brand_nationality = self.brand_nationality_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        expiry_date = self.expiry_date_entry.get()
        
        cursor = self.db_conn.cursor()

        if brand_nationality:
            cursor.execute("SELECT brand_id FROM brands ORDER BY brand_id DESC LIMIT 1")
            result = cursor.fetchone()
            new_brand_id = int(result[0]) + 1
            cursor.execute("INSERT INTO brands (brand_id, name, nationality) VALUES (?, ?, ?)", 
                           (new_brand_id, brand_name, brand_nationality))
            self.db_conn.commit()

        cursor.execute("SELECT name FROM items")
        items_names = cursor.fetchall()
        for n, i in enumerate(items_names):
            items_names[n] = i[0]
        cursor.execute("SELECT b.name FROM items AS i JOIN brands AS b ON i.brand_id = b.brand_id WHERE i.name = ?", (item_name,))
        brands = cursor.fetchall()
        cursor.execute("SELECT brand_id FROM brands WHERE name = ?", (brand_name,))
        brand_id = cursor.fetchone()[0]
        for n, i in enumerate(brands):
            brands[n] = i[0]
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
            cursor.execute('''
                INSERT INTO items (item_id, name, brand_id, price, quantity, expiry_date)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (item_id, item_name, brand_id, price, quantity, expiry_date))
            self.db_conn.commit()
            messagebox.showinfo("Success", "Item added successfully")

    def on_cart_click(self):
        pass
