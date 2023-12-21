import tkinter as tk
from screeninfo import get_monitors
import sqlite3
import login, signup, payment, cart, home, admin
import random

class MainApplication(tk.Tk):
    """
    Main application class representing the Tech Trolley application.
    """

    def __init__(self, geometry):
        """
        Initialize the main application.

        Parameters:
        - geometry (tuple): Tuple containing the width, height, x, and y coordinates of the main window.
        """
        super().__init__()
        
        # Set up the main window
        self.title("Tech Trolley")
        self.geometry_dims = geometry
        self.configure(bg="#d9f4ff")
        
        # Connect to the SQLite database
        self.conn = sqlite3.connect("techtrolley.db")

        # Configure grid weights for responsiveness
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialize variables
        self.email = None
        self.admin = None
        self.cart_id = None
        self.total_price = 0
        self.num_cart_items = 0

        # Initialize different pages of the application
        self.login_page = login.LoginPage(master=self, switch_to_signup_callback=self.switch_to_signup, 
                                          switch_to_home_callback=self.switch_to_home, db_conn=self.conn)
        self.signup_page = signup.SignUpPage(master=self, switch_to_login_callback=self.switch_to_login, 
                                             db_conn=self.conn, admin=self.admin)
        self.home_page = home.HomePage(master=self, switch_to_cart_callback=self.switch_to_cart, 
                                       switch_to_admin_callback=self.switch_to_admin, 
                                       switch_to_login_callback=self.switch_to_login, db_conn=self.conn, admin=self.admin, 
                                       customer_email=self.email, cart_id=self.cart_id)
        self.admin_page = admin.AdminPage(master=self, switch_to_home_callback=self.switch_to_home, 
                                          switch_to_signup_callback=self.switch_to_signup, db_conn=self.conn)
        self.cart_page = cart.CartPage(master=self, switch_to_payment_callback=self.switch_to_payment, 
                                       switch_to_home_callback=self.switch_to_home, db_conn=self.conn, cart_id=self.cart_id)
        self.payment_page = payment.PaymentPage(master=self, switch_to_cart_callback=self.switch_to_cart, 
                                                switch_to_home_callback=self.switch_to_home, db_conn=self.conn, 
                                                cart_id=self.cart_id, total_price=self.total_price, 
                                                num_cart_items=self.num_cart_items)
        
        # Set window size and position
        window_size = f"{self.geometry_dims[0]}x{self.geometry_dims[1]}+{self.geometry_dims[2]}+{self.geometry_dims[3]}"
        self.geometry(window_size)

        # Clean up old shopping carts
        cursor = self.conn.cursor()
        cursor.execute("""
            WITH to_be_deleted AS (
                SELECT item_id AS id, quantity AS n
                FROM cart_item AS ci
                JOIN shopping_carts AS sc
                ON ci.cart_id = sc.cart_id
                LEFT JOIN payments AS p
                ON sc.cart_id = p.cart_id
                WHERE p.payment_id IS NULL
                AND sc.creation_time <= DATE('now','-3 day')
            )
            UPDATE items
            SET quantity = quantity + n
            FROM to_be_deleted
            WHERE item_id = id
        """)
        cursor.execute("""
            DELETE FROM cart_item                 
            WHERE cart_id IN (                          
                SELECT sc.cart_id   
                FROM shopping_carts AS sc                   
                LEFT JOIN payments AS p                     
                ON sc.cart_id = p.cart_id                   
                WHERE p.payment_id IS NULL                    
                AND sc.creation_time <= DATE('now','-3 day')
            )
        """)
        cursor.execute("""
            DELETE FROM shopping_carts                 
            WHERE cart_id IN (                          
                SELECT sc.cart_id   
                FROM shopping_carts AS sc                   
                LEFT JOIN payments AS p                     
                ON sc.cart_id = p.cart_id                   
                WHERE payment_id IS NULL                    
                AND sc.creation_time <= DATE('now','-3 day')
            )
        """)
        self.conn.commit()
        cursor.execute("""
            SELECT item_id
            FROM items
            WHERE expiry_date >= DATE('now','-7 day')
        """)
        items = cursor.fetchall()
        for n, i in enumerate(items):
            items[n] = i[0]
        for i in items:
            cursor.execute("SELECT discount_id FROM discounts ORDER BY discount_id DESC LIMIT 1")
            result = cursor.fetchone()
            discount_id = int(result[0]) + 1
            discount = random.randint(5, 25)
            cursor.execute(f"""INSERT INTO discounts (discount_id, item_id, discount_amount, start_date, end_date)
                           VALUES ({discount_id}, {i}, {discount}, DATE('now'), DATE('now', '+7 day'))""")       
            self.conn.commit()
        self.switch_to_login()

    def switch_to_signup(self):
        """
        Switch to the signup page.
        """

        self.signup_page = signup.SignUpPage(master=self, switch_to_login_callback=self.switch_to_login, 
                                             db_conn=self.conn, admin=self.admin)
        self.login_page.grid_forget()
        self.home_page.grid_forget()
        self.admin_page.grid_forget()
        self.payment_page.grid_forget()
        self.cart_page.grid_forget()
        self.signup_page.grid(row=0, column=0, padx=10, pady=10)

    def switch_to_login(self):
        """
        Switch to the login page.
        """

        self.login_page = login.LoginPage(master=self, switch_to_signup_callback=self.switch_to_signup, 
                                          switch_to_home_callback=self.switch_to_home, db_conn=self.conn)
        self.signup_page.grid_forget()
        self.home_page.grid_forget()
        self.admin_page.grid_forget()
        self.payment_page.grid_forget()
        self.cart_page.grid_forget()
        self.login_page.grid(row=0, column=0, padx=10, pady=10)

    def switch_to_home(self):
        """
        Switch to the home page.
        """

        self.home_page = home.HomePage(master=self, switch_to_cart_callback=self.switch_to_cart, 
                                       switch_to_admin_callback=self.switch_to_admin, 
                                       switch_to_login_callback=self.switch_to_login, db_conn=self.conn, admin=self.admin, 
                                       customer_email=self.email, cart_id=self.cart_id)
        self.signup_page.grid_forget()
        self.login_page.grid_forget()
        self.admin_page.grid_forget()
        self.payment_page.grid_forget()
        self.cart_page.grid_forget()
        self.home_page.grid(row=0, column=0, sticky="nsew")

    def switch_to_admin(self):
        """
        Switch to the admin page.
        """

        self.admin_page = admin.AdminPage(master=self, switch_to_home_callback=self.switch_to_home, 
                                          switch_to_signup_callback=self.switch_to_signup, db_conn=self.conn)
        self.signup_page.grid_forget()
        self.login_page.grid_forget()
        self.home_page.grid_forget()
        self.admin_page.grid_forget()
        self.payment_page.grid_forget()
        self.cart_page.grid_forget()
        self.admin_page.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def switch_to_cart(self):
        """
        Switch to the cart page.
        """

        self.cart_page = cart.CartPage(master=self, switch_to_payment_callback=self.switch_to_payment, 
                                       switch_to_home_callback=self.switch_to_home, db_conn=self.conn, cart_id=self.cart_id)
        self.signup_page.grid_forget()
        self.login_page.grid_forget()
        self.home_page.grid_forget()
        self.admin_page.grid_forget()
        self.payment_page.grid_forget()
        self.cart_page.grid(row=0, column=0, sticky="nsew")

    def switch_to_payment(self):
        """
        Switch to the payment page.
        """
        
        self.payment_page = payment.PaymentPage(master=self, switch_to_cart_callback=self.switch_to_cart, 
                                                switch_to_home_callback=self.switch_to_home, db_conn=self.conn, 
                                                cart_id=self.cart_id, total_price=self.total_price, 
                                                num_cart_items=self.num_cart_items)
        self.signup_page.grid_forget()
        self.login_page.grid_forget()
        self.home_page.grid_forget()
        self.admin_page.grid_forget()
        self.cart_page.grid_forget()
        self.payment_page.grid(row=0, column=0, sticky="nsew")

@staticmethod
def getScreensInfo():
    """
    Get information about the screens (monitors).

    Returns:
    - tuple: Tuple containing the width, height, x, and y coordinates of the first screen.
    """
    
    monitors = get_monitors()
    first_screen = monitors[0]
    return first_screen.width, first_screen.height, first_screen.x, first_screen.y

if __name__ == "__main__":

    # Create and run the main application
    app = MainApplication(getScreensInfo())
    app.mainloop()