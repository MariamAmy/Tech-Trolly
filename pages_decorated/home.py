import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, font
from datetime import datetime, timedelta
from PIL import Image,ImageTk

class Item:
    """
    Represents an item in the shop.

    Attributes:
    - item_id: Unique identifier for the item.
    - name: Name of the item.
    - brand_name: Name of the brand.
    - brand_nationality: Nationality of the brand.
    - original_price: Original price of the item.
    - discount_price: Discounted price of the item.
    - sold: Total quantity sold.
    - sold_24h: Quantity sold in the last 24 hours.
    - discount: Boolean indicating if the item is on discount.
    - price: Final price after considering discounts.
    - quantity: Quantity of the item to be added to the cart.
    - quantity_in_store: Available quantity in the store.
    - discount_amount: Discount percentage.
    """

    def __init__(self, item_id, name, brand_name, brand_nationality, original_price, discount_price, 
                 sold, sold_24h, quantity, discount_amount, egyptian_share):
        """
        Initializes an Item object.

        Parameters:
        - item_id: Unique identifier for the item.
        - name: Name of the item.
        - brand_name: Name of the brand.
        - brand_nationality: Nationality of the brand.
        - original_price: Original price of the item.
        - discount_price: Discounted price of the item.
        - sold: Total quantity sold.
        - sold_24h: Quantity sold in the last 24 hours.
        - quantity: Quantity of the item in stock.
        - discount_amount: Discount percentage.
        """
        
        # Initialize item attributes
        self.item_id = item_id
        self.name = name
        self.brand_name = brand_name
        self.brand_nationality = brand_nationality
        self.original_price = original_price
        self.discount = not(original_price == discount_price)
        self.sold = sold
        self.sold_24h = sold_24h
        self.price = discount_price
        self.quantity = 0
        self.quantity_in_store = quantity
        self.discount_amount = discount_amount
        self.egyptian_share = egyptian_share

class ItemFrame(tk.Frame):
    """
    Represents a frame displaying an item with controls to change quantity and add to the cart.

    Attributes:
    - item: The Item object associated with the frame.
    - add_to_cart: Callback function to add the item to the cart.
    """

    def __init__(self, master, item, add_to_cart, *args, **kwargs):
        """
        Initializes an ItemFrame.

        Parameters:
        - master: The master widget.
        - item: The Item object associated with the frame.
        - add_to_cart: Callback function to add the item to the cart.
        """

        # Initialize ItemFrame
        super().__init__(master, *args, **kwargs)
        self.configure(bd=2, relief="groove")
        self.item = item
        self.add_to_cart = add_to_cart

        # Configure grid layout
        for i in range(7):
            self.grid_rowconfigure(i, weight=1)

        # Fetch stock quantity from the database
        cursor = master.master.master.master.master.db_conn.cursor()
        cursor.execute("SELECT quantity FROM items WHERE item_id = ?", (item.item_id,))
        self.stock_quantity = cursor.fetchone()[0]

        # Create widgets for the ItemFrame
        self.create_widgets()

    def create_widgets(self):
        """
        Create and configure the widgets for the item frame.
        """
        self.bg = "#f8f8f8"
        if self.item.egyptian_share == 100:
            self.bg = "#32CD32"
        self.configure(bg=self.bg)

        # Define the font styles
        label_font = font.Font(family="Arial", size=12)
        overstrike_font = font.Font(family="Arial", size=12, overstrike=True)
        button_font = font.Font(family="Arial", size=12, weight="bold")

        #Item Image
        self.item_image = (Image.open(f"images/{self.item.name}.png"))
        self.item_image = self.item_image.resize((200,200), Image.LANCZOS)
        self.item_image = ImageTk.PhotoImage(self.item_image)
        self.item_image_label = tk.Label(self, image=self.item_image, bg=self.bg)
        self.item_image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Item name label
        self.item_name_label = tk.Label(self, text=self.item.name, font=label_font, bg=self.bg)
        self.item_name_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        
        # Brand name label
        self.brand_name_label = tk.Label(self, text=self.item.brand_name, font=label_font, bg=self.bg)
        self.brand_name_label.grid(row=2, column=0, columnspan=3, padx=10, sticky="w")
        
        # Original price label
        self.item_ogprice_label = tk.Label(self, text=f"${self.item.original_price}", font=label_font, bg=self.bg)
        self.item_ogprice_label.grid(row=5, column=0, padx=10, sticky="w")

        # Discount percentage label
        self.item_discount_label = tk.Label(self, text=f" ", fg="red", font=label_font, bg=self.bg)
        self.item_discount_label.grid(row=4, column=0, padx=10, sticky="w")
        
        # If item is on discount, display discount information
        if self.item.discount:
            # Discounted price label
            self.item_newprice_label = tk.Label(self, text=f"${round(self.item.price, 2)}", font=label_font, bg=self.bg)
            self.item_newprice_label.grid(row=5, column=2, padx=10, sticky="e")
            self.item_discount_label.configure(text=f"{self.item.discount_amount}%")
            # Apply strikethrough to original price label
            self.item_ogprice_label.configure(font=overstrike_font)
        
        # Display a warning if the item quantity is low
        if self.item.quantity_in_store < 5:
            self.only_left_label = tk.Label(self, text=f"Only {self.item.quantity_in_store} left!", fg="red", font=label_font, bg=self.bg)
            self.only_left_label.grid(row=4, column=2, padx=10, sticky="e")
        
        # Sold and sold in the last 24 hours labels
        self.sold_label = tk.Label(self, text=f"Sold: {self.item.sold}", font=label_font, bg=self.bg)
        self.sold_label.grid(row=3, column=0, padx=10, sticky="w")
        self.sold24h_label = tk.Label(self, text=f"Sold in 24h: {self.item.sold_24h}", font=label_font, bg=self.bg)
        self.sold24h_label.grid(row=3, column=2, padx=10, sticky="e")

        # Quantity label
        self.quantity_label = tk.Label(self, text=f"Quantity: {self.item.quantity}", font=label_font, bg=self.bg)
        self.quantity_label.grid(row=6, column=1, padx=10)

        # Buttons to adjust quantity
        self.minus_button = tk.Button(self, text="-", command=self.decrease_quantity, font=button_font)
        self.minus_button.grid(row=6, column=0, padx=10, sticky="w")
        self.plus_button = tk.Button(self, text="+", command=self.increase_quantity, font=button_font)
        self.plus_button.grid(row=6, column=2, padx=10, sticky="e")

        # Button to add item to cart
        self.add_button = tk.Button(self, text="Add to Cart", command=lambda item=self.item: self.add_to_cart(item), font=button_font)
        self.add_button.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="ew")


    def increase_quantity(self):
        """
        Increase the quantity of the item in the frame.
        """

        # Check if there is enough stock
        if self.item.quantity < self.stock_quantity:
            self.item.quantity += 1
            self.quantity_label.config(text=f"Quantity: {self.item.quantity}")
        else:
            messagebox.showerror("Items", f"No more in stock")

    def decrease_quantity(self):
        """
        Decrease the quantity of the item in the frame.
        """

        # Check if the quantity is greater than 0
        if self.item.quantity > 0:
            self.item.quantity -= 1
            self.quantity_label.config(text=f"Quantity: {self.item.quantity}")

class HomePage(tk.Frame):
    """
    Represents the home page of the Tech Trolley application.

    Attributes:
    - switch_to_cart_callback: Callback function to switch to the cart page.
    - switch_to_admin_callback: Callback function to switch to the admin page.
    - db_conn: SQLite database connection.
    - cart_id: ID of the current shopping cart.
    - customer_email: Email address of the customer.
    - admin: Boolean indicating if the user is an admin.
    """

    def __init__(self, master, switch_to_cart_callback, switch_to_admin_callback, switch_to_login_callback, db_conn,
                 admin, customer_email, cart_id):
        """
        Initializes the HomePage.

        Parameters:
        - master: The master widget.
        - switch_to_cart_callback: Callback function to switch to the cart page.
        - switch_to_admin_callback: Callback function to switch to the admin page.
        - db_conn: SQLite database connection.
        - admin: Boolean indicating if the user is an admin.
        - customer_email: Email address of the customer.
        - cart_id: ID of the current shopping cart.
        """

        # Initialize HomePage
        super().__init__(master)
        self.switch_to_cart_callback = switch_to_cart_callback
        self.switch_to_admin_callback = switch_to_admin_callback
        self.switch_to_login_callback = switch_to_login_callback
        self.db_conn = db_conn
        self.admin = admin
        self.customer_email = customer_email
        self.cart_id = cart_id

        self.current_page = 1
        self.items_per_page = 50

        # Configure grid layout
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.configure(bg="#d9f4ff")

        # Create widgets for the home page
        self.create_widgets()

    def create_widgets(self):
        """
        Create and configure the widgets for the home page.
        """

        # Define the font styles
        title_font = font.Font(family="Arial", size=24, weight="bold")
        button_font = font.Font(family="Arial", size=12, weight="bold")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Create home frame and home button
        self.home_frame = tk.Frame(self, bg="#d9f4ff")
        self.home_frame.grid(row=0, column=0, sticky="nw", rowspan=2, padx=10, pady=10)
        self.button_home = tk.Button(self.home_frame, text="Home", font=button_font)
        self.button_home.pack(side="left", padx=5, pady=5)

        # Create admin button and configure its visibility
        self.button_admin = tk.Button(self, text="Admin Page", command=self.switch_to_admin_callback, font=button_font)
        if self.admin:
            self.button_admin.grid(row=0, column=1, sticky="n", pady=10)
        else:
            self.button_admin.grid_remove()

        # Market name label
        self.label_tech_trolley = tk.Label(self, text="Tech Trolley", font=title_font, bg="#d9f4ff")
        self.label_tech_trolley.grid(row=1, column=1)

        # Create cart frame and cart button
        self.original_cart_image = tk.PhotoImage(file="cart.png") 
        self.cart_image = self.original_cart_image.subsample(5, 5) 
        self.cart_frame = tk.Frame(self, bg="#d9f4ff")
        self.cart_frame.grid(row=0, column=2, sticky="ne", rowspan=2, padx=10, pady=10)
        self.button_cart = tk.Button(self.cart_frame, image=self.cart_image, compound="bottom", 
                                     command=self.switch_to_cart_callback, font=button_font)
        self.button_cart.pack(side="right", padx=5, pady=5)
        
        # Update cart button text based on the number of items in the cart
        self.num_cart_items = 0
        cursor = self.db_conn.cursor()
        if self.cart_id:
            cursor.execute("SELECT COUNT(*) FROM cart_item WHERE cart_id = ?", (self.cart_id,))
            self.num_cart_items = cursor.fetchone()[0]
        
        self.button_cart.configure(text=self.num_cart_items)

        # Create center frame for search, items, and filters
        self.center_frame = tk.Frame(self, bg="#d9f4ff")
        self.center_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)

        self.create_center_widgets()

    def create_center_widgets(self):
        """
        Create and configure the widgets for the center frame of the payment page.
        """
        # Define the font styles
        label_font = font.Font(family="Arial", size=12)
        entry_font = font.Font(family="Arial", size=12)
        button_font = font.Font(family="Arial", size=12, weight="bold")

        self.center_frame.grid_columnconfigure(0, weight=1)
        self.center_frame.grid_columnconfigure(1, weight=3)
        self.center_frame.grid_columnconfigure(2, weight=3)

        # Create search frame
        self.search_frame = tk.Frame(self.center_frame, bg="#d9f4ff")
        self.search_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        self.search_var = tk.StringVar()
        self.search_bar = tk.Entry(self.search_frame, textvariable=self.search_var, bg="#f8f8f8", font=entry_font)
        self.search_bar.pack(side="left", expand=True, fill="x", padx=10, pady=10, ipadx=5, ipady=5)
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.on_search_clicked, font=button_font)
        self.search_button.pack(side="right", padx=10, pady=10)

        # Items frame for displaying store items
        self.container = tk.Frame(self.center_frame, bg="#ffffff", bd=2, relief="groove")
        self.container.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=20, pady=10)
        self.center_canvas = tk.Canvas(self.container, bg="#ffffff", width=1530, height=750)
        self.center_canvas.pack(side="left", fill="both")
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.center_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.center_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.items_frame = tk.Frame(self.center_canvas, bg="#ffffff")
        self.items_frame_window_id = self.center_canvas.create_window((0, 0), window=self.items_frame, anchor="nw")
        self.center_canvas.bind_all("<MouseWheel>", 
                                    lambda event: self.center_canvas.yview_scroll(-1 * (event.delta // 120), "units"))
        
        self.item_frames = []
        self.shop_items = []

        self.left_frame = tk.Frame(self.center_frame, bg="#ffffff", bd=2, relief="groove")
        self.left_frame.grid(row=1, column=0, sticky="nws", padx=10, pady=10)

        self.filter_frame = tk.Frame(self.left_frame, bg="#ffffff")
        self.filter_frame.pack(side="top", fill="both", padx=10, pady=10)

        self.filter_label = tk.Label(self.filter_frame, text="Filter By", font=button_font, bg="#ffffff")
        self.filter_label.grid(row=0, column=0, padx=10, pady=20)

        # Brand Name filter
        cursor = self.db_conn.cursor()
        self.brand_name_var = tk.StringVar()
        self.brand_name_combo = ttk.Combobox(self.filter_frame, textvariable=self.brand_name_var, font=entry_font)
        cursor.execute("SELECT DISTINCT name FROM brands")
        brands = cursor.fetchall()
        for n, i in enumerate(brands):
                brands[n] = i[0]
        self.brand_name_combo["values"] = ["Select Brand"] + brands
        self.brand_name_combo.grid(row=1, column=0, padx=10, pady=10)
        self.brand_name_combo.set("Select Brand")
        self.brand_name_combo.bind("<<ComboboxSelected>>", self.on_brand_name_changed)

        # Brand Nationality filter
        self.brand_nationality_var = tk.StringVar()
        self.brand_nationality_combo = ttk.Combobox(self.filter_frame, textvariable=self.brand_nationality_var, font=entry_font)
        cursor.execute("SELECT DISTINCT nationality FROM brands")
        nationalities = cursor.fetchall()
        for n, i in enumerate(nationalities):
                nationalities[n] = i[0]
        self.brand_nationality_combo["values"] = ["Select Nationality"] + nationalities
        self.brand_nationality_combo.grid(row=2, column=0, padx=10, pady=10)
        self.brand_nationality_combo.set("Select Nationality")
        self.brand_nationality_combo.bind("<<ComboboxSelected>>", self.on_brand_nationality_changed)

        # Category filter
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(self.filter_frame, textvariable=self.category_var, font=entry_font)
        categories = ["Dairy", "Bakery", "Beverages", "Snacks", "Meat", "Seafood", "Produce", "Canned Goods", 
                      "Frozen Food", "Personal Care"]
        self.category_combo["values"] = ["Select Category"] + categories
        self.category_combo.grid(row=3, column=0, padx=10, pady=10)
        self.category_combo.set("Select Category")
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_changed)

        # Price filters
        cursor.execute("SELECT MAX(price), MIN(price) FROM items")
        max_price, min_price = cursor.fetchone()
        
        self.min_price_label = tk.Label(self.filter_frame, text="Min Price", font=label_font, bg="#ffffff")
        self.min_price_label.grid(row=4, column=0, padx=10, pady=10)
        self.min_price = tk.Scale(self.filter_frame, from_=min_price, to=max_price, orient=tk.HORIZONTAL, font=label_font, 
                                  command=self.update_max_price, bd=2, relief="groove")
        self.min_price.bind("<ButtonRelease-1>", self.button_release)
        self.min_price.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.max_price_label = tk.Label(self.filter_frame, text="Max Price", font=label_font, bg="#ffffff")
        self.max_price_label.grid(row=6, column=0, padx=10, pady=10)
        self.max_price = tk.Scale(self.filter_frame, from_=min_price, to=max_price, orient=tk.HORIZONTAL, font=label_font, 
                                  command=self.update_min_price, bd=2, relief="groove")
        self.max_price.bind("<ButtonRelease-1>", self.button_release)
        self.max_price.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.min_price.set(min_price)
        self.max_price.set(max_price)

        # Discount filter
        self.discount_check_var = tk.IntVar() 
        self.on_discount_check = tk.Checkbutton(self.filter_frame, text="On discount", variable=self.discount_check_var, 
                                                font=label_font, command=self.on_discount_checked, bg="#ffffff")
        self.on_discount_check.grid(row=8, column=0, padx=10, pady=10)

        # Bottom frame
        self.logout_frame = tk.Frame(self.left_frame, bg="#ffffff")
        self.logout_frame.pack(side="bottom", padx=10, pady=10)

        # Buttons for switching between pages
        self.prev_page_button = tk.Button(self.logout_frame, text="<", command=self.switch_to_previous_page,
                                          font=button_font)
        self.prev_page_button.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        if self.current_page == 1:
            self.prev_page_button.config(state="disabled")
        else:
            self.prev_page_button.config(state="normal")

        self.next_page_button = tk.Button(self.logout_frame, text=">", command=self.switch_to_next_page,
                                          font=button_font)
        self.next_page_button.grid(row=0, column=2, padx=10, pady=10, columnspan=2)

        # Logout Button
        self.logout_button = tk.Button(self.logout_frame, text="Log Out", font=button_font, command=self.log_out)
        self.logout_button.grid(row=1, column=0, columnspan=3, sticky="sew")

        # Fetch and display items
        self.fetch_items()

        # Update visibility of add to cart buttons based on cart contents
        self.add_to_cart_button_visibilty()

        self.center_canvas.bind("<Configure>", lambda e: self.on_canvas_configure(e.width))

    def button_release(self, event):
        """
        Update items on button release of price filter.
        """

        self.current_page = 1
        self.fetch_items()

    def on_canvas_configure(self, canvas_width):
        """
        Update the scrollregion of the canvas to the size of the items_frame.
        """
        self.center_canvas.configure(scrollregion=self.center_canvas.bbox("all"))

        # Calculate the positions to center the items_frame
        items_frame_width = self.items_frame.winfo_reqwidth()

        # Calculate the center position
        x_position = max(0, (canvas_width - items_frame_width) / 2)

        # Move the items_frame to the center position
        self.center_canvas.coords(self.items_frame_window_id, x_position, 0)

    def switch_to_previous_page(self):
        """
        Switch to the previous page and update the items.
        """

        if self.current_page > 1:
            self.current_page -= 1
            self.fetch_items()
            self.next_page_button.config(state="normal")

        # Disable previous page button when on the first page
        if self.current_page == 1:
            self.prev_page_button.config(state="disabled")

    def switch_to_next_page(self):
        """
        Switch to the next page and update the items.
        """
        self.current_page += 1
        self.fetch_items()

        # Check if there are items on the next page
        if len(self.shop_items) < self.items_per_page:
            self.next_page_button.config(state="disabled")
        else:
            self.next_page_button.config(state="normal")

        # Enable previous page button
        self.prev_page_button.config(state="normal")

    def update_min_price(self, val):
        """
        Update the minimum price filter based on the slider value.

        Parameters:
        - val: The current slider value.
        """

        min_val = self.min_price.get()
        max_val = int(val)
        if max_val < min_val:
            self.min_price.set(max_val)

    def update_max_price(self, val):
        """
        Update the maximum price filter based on the slider value.

        Parameters:
        - val: The current slider value.
        """

        max_val = self.max_price.get()
        min_val = int(val)
        if min_val > max_val:
            self.max_price.set(min_val)
    
    def on_brand_name_changed(self, event=None):
        """
        Callback function for brand name filter change.

        Parameters:
        - event: Event object (default is None).
        """

        self.current_page = 1
        self.fetch_items()

    def on_brand_nationality_changed(self, event=None):
        """
        Callback function for brand nationality filter change.

        Parameters:
        - event: Event object (default is None).
        """

        self.current_page = 1
        self.fetch_items()

    def on_category_changed(self, event=None):
        """
        Callback function for category filter change.

        Parameters:
        - event: Event object (default is None).
        """

        self.current_page = 1
        self.fetch_items()

    def on_discount_checked(self):
        """
        Callback function for on discount filter change.
        """

        self.current_page = 1
        self.fetch_items()
    
    def on_search_clicked(self):
        """
        Callback function for search button click.
        """

        self.current_page = 1
        self.fetch_items()

    def display_items(self):
        """
        Display items on the home page.
        """

        for i in self.item_frames:
            i.destroy()
        self.item_frames = []
        for i, item in enumerate(self.shop_items):
            row = i // 4
            column = i % 4
            frame = ItemFrame(self.items_frame, item, self.add_to_cart)
            frame.grid(row=row, column=column, padx=5, pady=5, sticky="ew")
            self.item_frames.append(frame)
        
        self.items_frame.update_idletasks()
        self.on_canvas_configure(self.center_canvas.winfo_width())

    def fetch_items(self):
        """
        Fetch items based on selected filters and current page.
        """

        offset = (self.current_page - 1) * self.items_per_page
        limit = self.items_per_page

        self.shop_items = []
        current_time = datetime.now()
        one_day_ago = current_time - timedelta(days=1)
        cursor = self.db_conn.cursor()

        brand_name_filter = self.brand_name_var.get()
        brand_nationality_filter = self.brand_nationality_var.get()
        category_filter = self.category_var.get()
        min_price_filter = self.min_price.get()
        max_price_filter = self.max_price.get()
        on_discount_filter = self.discount_check_var.get()
        search_filter = self.search_var.get()

        query = """
            SELECT i.item_id, i.name, i.quantity, i.price, b.name, b.nationality,
            (SELECT SUM(quantity) FROM cart_item WHERE item_id = i.item_id) AS sold,
            (SELECT SUM(quantity) FROM cart_item AS ci JOIN payments AS p ON ci.cart_id = p.cart_id WHERE p.payment_date >= ?)
            AS sold_24h,
            (SELECT discount_amount FROM discounts WHERE item_id = i.item_id AND start_date <= ? AND end_date >= ?) AS discount,
            (SELECT SUM(share) FROM stakeholders WHERE nationality = 'Egyptian' AND brand_id = i.brand_id GROUP BY brand_id) AS egyptian_share
            FROM items i
            JOIN brands b ON i.brand_id = b.brand_id
        """
        values = (one_day_ago, current_time, current_time)
        filters = []

        if brand_name_filter and brand_name_filter != "Select Brand":
            filters.append("b.name = ?")
            values += (brand_name_filter,)

        if brand_nationality_filter and brand_nationality_filter != "Select Nationality":
            filters.append("b.nationality = ?")
            values += (brand_nationality_filter,)
        
        if category_filter and category_filter != "Select Category":
            filters.append("i.name LIKE ?")
            values += (f"%{category_filter}%",)

        if min_price_filter:
            filters.append("i.price >= ?")
            values += (min_price_filter,)

        if max_price_filter:
            filters.append("i.price <= ?")
            values += (max_price_filter,)

        if on_discount_filter:
            filters.append("i.item_id IN (SELECT item_id FROM discounts)")

        if search_filter:
            filters.append("(i.name LIKE ? OR b.name LIKE ?)")
            values += (f"%{search_filter}%", f"%{search_filter}%")

        if filters:
            query += " WHERE " + " AND ".join(filters)
        
        query += " LIMIT ? OFFSET ?"
        values += (limit, offset)
        
        cursor.execute(query, values)

        for row in cursor.fetchall():
            item_id, item_name, item_quantity, item_price, brand_name, \
            brand_nationality, sold, sold_24h, discount, egyptian_share = row
            sold_24h = sold_24h if sold_24h else 0
            if discount:
                discount_price = item_price * (1 - (discount / 100))
            else:
                discount_price = item_price
            if item_quantity > 0:
                item = Item(item_id, item_name, brand_name, brand_nationality, item_price, discount_price, sold, sold_24h, 
                            item_quantity, discount, egyptian_share)
                self.shop_items.append(item)

        # Disable previous page button when on the first page
        if self.current_page == 1:
            self.prev_page_button.config(state="disabled")
        else:
            self.prev_page_button.config(state="normal")

        # Check if there are items on the next page
        if len(self.shop_items) < self.items_per_page:
            self.next_page_button.config(state="disabled")
        else:
            self.next_page_button.config(state="normal")

        self.display_items()
    
    def add_to_cart(self, item):
        """
        Add the selected item to the cart.

        Parameters:
        - item: The selected Item object.
        """
        if item.quantity > 0:
            cursor = self.db_conn.cursor()
            if not self.cart_id:
                cursor.execute("SELECT cart_id FROM shopping_carts ORDER BY cart_id DESC LIMIT 1")
                result = cursor.fetchone()
                self.cart_id = int(result[0]) + 1
                self.master.cart_id = self.cart_id
                cursor.execute("INSERT INTO shopping_carts (cart_id, customer_email, creation_time) VALUES (?, ?, ?)", 
                                    (self.cart_id, self.customer_email, datetime.now()))
                self.db_conn.commit()
            
            cursor.execute("INSERT INTO cart_item (cart_id, item_id, quantity) VALUES (?, ?, ?)", (self.cart_id, item.item_id, item.quantity))
            self.db_conn.commit()
            cursor.execute("UPDATE items SET quantity = quantity - ? WHERE item_id = ?", (item.quantity, item.item_id))
            self.db_conn.commit()
            cursor.execute("SELECT COUNT(*) FROM cart_item WHERE cart_id = ?", (self.cart_id,))
            self.num_cart_items = cursor.fetchone()[0]
            self.button_cart.configure(text=self.num_cart_items)
            self.add_to_cart_button_visibilty()
            messagebox.showinfo("Cart", f"Added {item.quantity} of {item.name} to the cart.")
        
        else:
            messagebox.showerror("Cart", "No quantity selected")

    def add_to_cart_button_visibilty(self):
        """
        Update visibility of add to cart buttons based on cart contents.
        """

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

    def log_out(self):
        """
        Log out and restore all global variables to the default.
        """
        self.master.email = None
        self.master.admin = None
        self.master.cart_id = None
        self.master.total_price = 0
        self.master.num_cart_items = 0
        self.switch_to_login_callback()
        