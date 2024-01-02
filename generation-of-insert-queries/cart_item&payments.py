import random
from faker import Faker
from datetime import timedelta

# Constants
N_CARTS = 120
N_ITEMS = 1000
N_PAYMENTS = 110
N_CART_ITEMS = 5000

# Sets to keep track of generated data
generated_carts = {}

# Instantiate a Faker object
fake = Faker()

def generate_payment_method():
    """
    Generate a random payment method.

    Returns:
    - str: The generated payment method.
    """
    methods = ['Credit Card', 'Debit Card', 'Paypal', 'Cash on Delivery', 'Bank Transfer']
    return random.choice(methods)

def random_datetime_within_range(start_datetime, end_datetime):
    """
    Generate a random datetime within a given range.

    Parameters:
    - start_datetime (datetime): Start of the date range.
    - end_datetime (datetime): End of the date range.

    Returns:
    - datetime: The generated random datetime.
    """
    delta = end_datetime - start_datetime
    random_seconds = random.uniform(0, delta.total_seconds())
    return start_datetime + timedelta(seconds=random_seconds)

def generate_payments_insert_statements(num_records):
    """
    Generate INSERT statements for the 'payments' table.

    Parameters:
    - num_records (int): Number of payment records to generate.

    Returns:
    - list: List of INSERT statements for payments.
    """
    insert_statements = []
    payment_id = 0
    called_carts = set()
    
    for _ in range(num_records):
        while True:
            cart_id = random.randint(1, N_CARTS)
            if cart_id not in called_carts:
                called_carts.add(cart_id)
                break

        creation_time = generated_carts[cart_id]
        end_time = creation_time + timedelta(days=3)
        total_price = round(random.uniform(5.0, 1000.0), 2)
        payment_method = generate_payment_method()
        payment_date = random_datetime_within_range(creation_time, end_time)

        insert_statement = f"INSERT INTO payments (payment_id, cart_id, total_price, payment_method, payment_date) VALUES ({payment_id}, {cart_id}, {total_price}, '{payment_method}', '{payment_date}');"
        insert_statements.append(insert_statement)
        payment_id += 1
        
    return insert_statements

def generate_cart_item_insert_statements(num_records):
    """
    Generate INSERT statements for the 'cart_item' table.

    Parameters:
    - num_records (int): Number of cart item records to generate.

    Returns:
    - list: List of INSERT statements for the 'cart_item' table.
    """
    insert_statements = []
    called_cart_items = []

    for _ in range(num_records):
        while True:
            cart_id = random.randint(1, N_CARTS)
            item_id = random.randint(1, N_ITEMS)
            if [cart_id, item_id] not in called_cart_items:
                called_cart_items.append([cart_id, item_id])
                break
        quantity = random.randint(1, 10)
        
        insert_statement = f"INSERT INTO cart_item (cart_id, item_id, quantity) VALUES ({cart_id}, {item_id}, {quantity});"
        insert_statements.append(insert_statement)
    
    return insert_statements

# Generate INSERT statements for the 'cart_item' table
cart_item_insert_queries = generate_cart_item_insert_statements(N_CART_ITEMS)

# Generate INSERT statements for the 'payments' table
payments_insert_queries = generate_payments_insert_statements(N_PAYMENTS)