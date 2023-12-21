import tkinter as tk
from tkinter import messagebox, font

class CartPage(tk.Frame):
    """
    Represents the shopping cart page of the Tech Trolley application.

    Attributes:
    - master: The master widget.
    - switch_to_payment_callback: Callback function to switch to the payment page.
    - switch_to_home_callback: Callback function to switch to the home page.
    - db_conn: SQLite database connection.
    - cart_id: ID of the current shopping cart.
    """

    def __init__(self, master, switch_to_payment_callback, switch_to_home_callback, db_conn, cart_id):
        """
        Initialize the CartPage.

        Parameters:
        - master: The master widget.
        - switch_to_payment_callback: Callback function to switch to the payment page.
        - switch_to_home_callback: Callback function to switch to the home page.
        - db_conn: SQLite database connection.
        - cart_id: ID of the current shopping cart.
        """

        super().__init__(master)
        self.db_conn = db_conn
        self.cart_id = cart_id
        self.switch_to_payment_callback = switch_to_payment_callback
        self.switch_to_home_callback = switch_to_home_callback

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.configure(bg="#d9f4ff")

        self.create_widgets()
        self.fetch_and_display_cart_items()
        self.fetch_num_cart_items()

    def create_widgets(self):
        """
        Create and configure the widgets for the cart page.
        """

        # Define the font styles
        button_font = font.Font(family="Arial", size=12, weight="bold")

        # Home button
        self.home_frame = tk.Frame(self, bg="#d9f4ff")
        self.home_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        self.button_home = tk.Button(self.home_frame, text="Home", command=self.switch_to_home_callback, font=button_font)
        self.button_home.pack(side="left", padx=5, pady=5)

        # Load the image for the cart button and resize it
        self.original_cart_image = tk.PhotoImage(file="cart.png") 
        self.cart_image = self.original_cart_image.subsample(5, 5)

        # Cart button
        self.cart_frame = tk.Frame(self, bg="#d9f4ff")
        self.cart_frame.grid(row=0, column=2, sticky="ne", padx=10, pady=10)
        self.button_cart = tk.Button(self.cart_frame, image=self.cart_image, compound = "bottom", font=button_font)
        self.button_cart.pack(side="right", padx=5, pady=5)

        # Center frame for displaying cart items
        self.container = tk.Frame(self, bg="#ffffff", bd=2, relief="groove")
        self.container.grid(row=1, column=1, sticky="nsew", padx=50, pady=50)
        self.center_canvas = tk.Canvas(self.container, bg="#ffffff", width=800, height=500)
        self.center_canvas.pack(side="left", fill="both")
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.center_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.center_canvas.configure(yscrollcommand=self.scrollbar.set)

        # center frame inside Canvas
        self.center_frame = tk.Frame(self.center_canvas, bg="#ffffff", pady=30)
        self.center_frame_window_id = self.center_canvas.create_window((0, 0), window=self.center_frame, anchor="nw")
        self.center_canvas.bind_all("<MouseWheel>", 
                                    lambda event: self.center_canvas.yview_scroll(-1 * (event.delta // 120), "units"))

        # List to store frames displaying each item in the cart
        self.item_frames = []

        # Display cart items
        self.update_item_frames()

        # Proceed to payment button
        self.btn_proceed = tk.Button(self, text="Proceed to Payment", command=self.switch_to_payment_callback_check, 
                                     font=button_font)
        self.btn_proceed.grid(row=2, column=1, pady=50, sticky="s")
        
        self.center_canvas.bind("<Configure>", lambda e: self.on_canvas_configure(e.width))

    def on_canvas_configure(self, canvas_width):
        """
        Update the scrollregion of the canvas to the size of the center_frame
        """
        self.center_canvas.configure(scrollregion=self.center_canvas.bbox("all"))

        # Calculate the positions to center the center_frame
        center_frame_width = self.center_frame.winfo_reqwidth()

        # Calculate the center position
        x_position = max(0, (canvas_width - center_frame_width) / 2)

        # Move the center_frame to the center position
        self.center_canvas.coords(self.center_frame_window_id, x_position, 0)
            
    def update_item_frames(self):
        """
        Update the frames displaying each item in the cart.
        """

        # Destroy existing item frames
        for frame in self.item_frames:
            for i in frame:
                i.destroy()

        self.item_frames.clear()
        self.fetch_and_display_cart_items()

        # Define the font styles
        button_font = font.Font(family="Arial", size=12, weight="bold")
        label_font = font.Font(family="Arial", size=14)

        lbl1 = tk.Label(self.center_frame, text="Item Name", bg="#ffffff", font=label_font)
        lbl1.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        lbl2 = tk.Label(self.center_frame, text="Item Price", bg="#ffffff", font=label_font)
        lbl2.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        lbl3 = tk.Label(self.center_frame, text="Quantity", bg="#ffffff", font=label_font)
        lbl3.grid(row=0, column=3, padx=5, pady=5)

        lbl4 = tk.Label(self.center_frame, text="Total Price", bg="#ffffff", font=label_font)
        lbl4.grid(row=0, column=5, padx=5, pady=5, sticky="e")
        
        # Clear out any existing item frames
        for frame in self.item_frames:
            for i in frame:
                i.destroy()
        self.item_frames.clear()

        # Create a frame for each cart item
        for i, (item_id, name, price, quantity) in enumerate(self.cart_items, start=1):
            lbl_item_name = tk.Label(self.center_frame, text=name, bg="#ffffff", font=label_font)
            lbl_item_name.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            lbl_price = tk.Label(self.center_frame, text=f"${price:.2f}", bg="#ffffff", font=label_font)
            lbl_price.grid(row=i, column=1, padx=5, pady=5, sticky="w")

            btn_minus = tk.Button(self.center_frame, text="-", font=button_font,
                                  command=lambda item_id = item_id, name = name: self.update_quantity(item_id, name, -1))
            btn_minus.grid(row=i, column=2, padx=5, pady=5, sticky="w")
            lbl_quantity = tk.Label(self.center_frame, text=str(quantity), bg="#ffffff", font=label_font)
            lbl_quantity.grid(row=i, column=3, padx=5, pady=5)
            btn_plus = tk.Button(self.center_frame, text="+", font=button_font,
                                 command=lambda item_id = item_id, name = name: self.update_quantity(item_id, name, 1))
            btn_plus.grid(row=i, column=4, padx=5, pady=5, sticky="w")

            lbl_total = tk.Label(self.center_frame, text=f"${price * quantity:.2f}", bg="#ffffff", font=label_font)
            lbl_total.grid(row=i, column=5, padx=5, pady=5, sticky="e")
            self.item_frames.append([lbl_item_name, lbl_price, btn_minus, lbl_quantity, btn_plus, lbl_total])
        
        # Create a total frame for displaying the cart total
        self.total_frame = tk.Frame(self.center_frame,bg="#ffffff")
        self.total_frame.grid(row=len(self.cart_items) + 1, column=0, columnspan=6, pady=20, sticky="ew")

        # Configure column weights for the total frame
        for col in range(6):
            self.total_frame.grid_columnconfigure(col, weight=1)

        self.lbl_cart_total_text = tk.Label(self.total_frame, text="Cart Total:", bg="#ffffff", font=label_font)
        self.lbl_cart_total_text.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.lbl_cart_total = tk.Label(self.total_frame, text=f"${self.calculate_total():.2f}", bg="#ffffff", font=label_font)
        self.lbl_cart_total.grid(row=0, column=5, sticky="e")

        self.center_frame.update_idletasks()
        self.on_canvas_configure(self.center_canvas.winfo_width())

    def switch_to_payment_callback_check(self):
        """
        Switch to the payment page.
        """
        
        self.fetch_num_cart_items()
        # Check if there are items in the cart
        if self.num_cart_items:
            self.switch_to_payment_callback()
        else:
            messagebox.showinfo("Cart", "Your cart is empty. Please add items before proceeding to payment.")

    def fetch_num_cart_items(self):
        """
        Fetch and update the number of items in the cart.
        """

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT COUNT(i.name) \
                       FROM items AS i \
                       JOIN cart_item AS ci \
                       ON i.item_id = ci.item_id \
                       WHERE ci.cart_id = ?", (self.cart_id,))
        self.num_cart_items = cursor.fetchone()[0]
        self.master.num_cart_items = self.num_cart_items
        self.button_cart.configure(text=self.num_cart_items)

    def fetch_and_display_cart_items(self):
        """
        Fetch and display the items in the cart.
        """

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT i.item_id, i.name, i.price, ci.quantity \
                       FROM items AS i \
                       JOIN cart_item AS ci \
                       ON i.item_id = ci.item_id \
                       WHERE ci.cart_id = ?", (self.cart_id,))
        self.cart_items = cursor.fetchall()

    def update_quantity(self, item_id, name, change):
        """
        Update the quantity of an item in the cart.

        Parameters:
        - item_id: ID of the item to be updated.
        - name: Name of the item.
        - change: The change in quantity (1 for increase, -1 for decrease).
        """

        cursor = self.db_conn.cursor()

        # Decrease quantity and update stock if decreasing
        if change == -1:
            cursor.execute("UPDATE cart_item SET quantity = quantity - 1 WHERE cart_id = ? AND item_id = ?", (self.cart_id, item_id))
            cursor.execute("UPDATE items SET quantity = quantity + 1 WHERE item_id = ?", (item_id,))
        else:
            # Check stock before increasing quantity
            cursor.execute("SELECT quantity FROM items WHERE item_id = ?", (item_id,))
            self.stock_quantity = cursor.fetchone()[0]
            if self.stock_quantity > 0:
                cursor.execute("UPDATE cart_item SET quantity = quantity + 1 WHERE cart_id = ? AND item_id = ?", (self.cart_id, item_id))
                cursor.execute("UPDATE items SET quantity = quantity - 1 WHERE item_id = ?", (item_id,))
            else:
                messagebox.showerror("Items", f"No more in stock")

        # Commit changes to the database
        self.db_conn.commit()

        # Update the cart total label
        self.lbl_cart_total.configure(text=f"${self.calculate_total():.2f}")

        # Fetch the new quantity
        cursor.execute("SELECT quantity FROM cart_item WHERE cart_id = ? AND item_id = ?", (self.cart_id, item_id))
        new_quantity = cursor.fetchone()[0]

        # Check if the quantity is zero or less, and confirm deletion
        if new_quantity <= 0:
            response = messagebox.askokcancel("Confirm Deletion", f"Are you sure you want to remove {name} from your cart?")
            if response:
                # Remove the item from the cart
                cursor.execute("DELETE FROM cart_item WHERE cart_id = ? AND item_id = ?", (self.cart_id, item_id))
                messagebox.showinfo("Cart", f"Item {name} has been removed from your cart.")
                if self.num_cart_items <= 0:
                    cursor.execute("DELETE FROM shopping_carts WHERE cart_id = ?", (self.cart_id,))
                    self.cart_id = None
                    self.master.cart_id = None
            else:
                # Revert changes if deletion is canceled
                cursor.execute("UPDATE cart_item SET quantity = quantity + 1 WHERE cart_id = ? AND item_id = ?", (self.cart_id, item_id))
                cursor.execute("UPDATE items SET quantity = quantity - 1 WHERE item_id = ?", (item_id,))

        # Commit changes to the database
        self.db_conn.commit()

        # Update the number of cart items and refresh the item frames
        self.fetch_num_cart_items()
        self.button_cart.configure(text=self.num_cart_items)
        self.total_frame.destroy()
        self.update_item_frames()

    def calculate_total(self):
        """
        Calculate the total price of items in the cart.

        Returns:
        - float: The total price.
        """
        
        cursor = self.db_conn.cursor()
        cursor.execute("""SELECT SUM(i.price * ci.quantity)
                       FROM items AS i
                       JOIN cart_item AS ci
                       ON i.item_id = ci.item_id
                       WHERE ci.cart_id = ?""", (self.cart_id,))
        total = cursor.fetchone()[0]
        self.master.total_price = total
        return total if total else 0.0
