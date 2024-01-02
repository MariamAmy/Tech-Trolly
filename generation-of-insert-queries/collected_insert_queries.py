import random
import hashlib
import numpy as np
from faker import Faker
from datetime import timedelta

# Constants
N_CUSTOMERS = 100
N_ITEMS = 1000
N_BRANDS = 100
N_CARTS = 120
N_CART_ITEMS = 5000
N_PAYMENTS = 110
N_DISCOUNTS = 200
N_PROMOCODES = 50
N_PAYMENT_PROMOCODE = int(0.2*N_PAYMENTS)

# Sets to keep track of generated data
generated_emails = set()
generated_promocodes = set()
generated_brand_names = set()
generated_carts = {}

# Instantiate a Faker object
fake = Faker()

def hash_password(password):
    """
    Hash a password using SHA-256.

    Parameters:
    - password (str): The password to be hashed.

    Returns:
    - str: The hashed password.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_phone_number():
    """
    Generate a random Egyptian phone number.

    Returns:
    - str: The generated phone number.
    """
    prefixes = ['+2010', '+2011', '+2012', '+2015']
    return random.choice(prefixes) + ''.join(random.choice('0123456789') for _ in range(8))

def generate_customer_insert_statements(num_records):
    """
    Generate INSERT statements for the 'customers' table.

    Parameters:
    - num_records (int): Number of customer records to generate.

    Returns:
    - list: List of INSERT statements for customers.
    """
    insert_statements = []
    
    for _ in range(num_records):
        email = fake.email()
        while email in generated_emails:
            email = fake.email()
        generated_emails.add(email)
        password = hash_password(fake.password(length=12))
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone_number = generate_phone_number()
        
        insert_statement = f"INSERT INTO customers (email, password, first_name, last_name, phone_number) VALUES ('{email}', '{password}', '{first_name}', '{last_name}', '{phone_number}');"
        insert_statements.append(insert_statement)
    
    return insert_statements

def generate_expiration_date():
    """
    Generate a random expiration date for items.

    Returns:
    - date: The generated expiration date.
    """
    return fake.date_between(start_date="today", end_date="+5y")

def generate_supermarket_item_name():
    """
    Generate a realistic item name for a supermarket.

    Returns:
    - str: The generated item name.
    """
    categories = ['Dairy', 'Bakery', 'Beverages', 'Snacks', 'Meat', 'Seafood', 'Produce', 'Canned Goods', 'Frozen Food', 'Personal Care']
    item_types = {
        'Dairy': ['Milk', 'Cheese', 'Yogurt', 'Butter', 'Cream', 'Eggs', 'Cottage Cheese', 'Whipping Cream'],
        'Bakery': ['Bread', 'Cookies', 'Cake', 'Muffins', 'Pies', 'Bagels', 'Croissants', 'Donuts'],
        'Beverages': ['Juice', 'Soda', 'Water', 'Tea', 'Coffee', 'Energy Drink', 'Smoothie', 'Iced Tea'],
        'Snacks': ['Chips', 'Nuts', 'Candy', 'Chocolate', 'Popcorn', 'Pretzels', 'Granola Bars', 'Trail Mix'],
        'Meat': ['Chicken', 'Beef', 'Pork', 'Lamb', 'Turkey', 'Bacon', 'Sausages', 'Ham'],
        'Seafood': ['Fish', 'Shrimp', 'Crab', 'Lobster', 'Oysters', 'Squid', 'Salmon', 'Tuna'],
        'Produce': ['Apples', 'Bananas', 'Tomatoes', 'Lettuce', 'Carrots', 'Cucumbers', 'Oranges', 'Avocado'],
        'Canned Goods': ['Beans', 'Soup', 'Corn', 'Peas', 'Tomato Sauce', 'Tuna', 'Pasta Sauce', 'Vegetable Broth'],
        'Frozen Food': ['Pizza', 'Dumplings', 'Ice Cream', 'Berries', 'Vegetables', 'Frozen Meals', 'Frozen Pies', 'Frozen Waffles'],
        'Personal Care': ['Soap', 'Shampoo', 'Toothpaste', 'Lotion', 'Deodorant', 'Shaving Cream', 'Mouthwash', 'Hair Gel']
    }
    
    category = random.choice(categories)
    item_name = random.choice(item_types[category])
    
    return f"{category} {item_name}"

def generate_items_insert_statements(num_records):
    """
    Generate INSERT statements for the 'items' table with realistic item names.

    Parameters:
    - num_records (int): Number of item records to generate.

    Returns:
    - list: List of INSERT statements for items.
    """
    item_id = 1
    insert_statements = []
    
    for _ in range(num_records):
        name = generate_supermarket_item_name()
        quantity = random.randint(1, 100)
        price = round(random.uniform(0.5, 100.0), 2)
        brand_id = random.randint(1, N_BRANDS)
        expiry_date = generate_expiration_date()
        
        insert_statement = f"INSERT INTO items (item_id, name, quantity, price, brand_id, expiry_date) VALUES ({item_id}, '{name}', {quantity}, {price}, {brand_id}, '{expiry_date}');"
        insert_statements.append(insert_statement)
        item_id += 1
    return insert_statements

def generate_supermarket_brand_name():
    """
    Generate a realistic brand name for a supermarket.

    Returns:
    - str: The generated brand name.
    """
    adjectives = ['Golden', 'Fresh', 'Pure', 'Organic', 'Natural', 'Tasty', 'Quality', 'Premium', 'Classic', 'Delicious', 'Wholesome']
    food_terms = ['Harvest', 'Fields', 'Gardens', 'Orchard', 'Market', 'Kitchen', 'Delights', 'Farms', 'Bounty', 'Freshness', 'Nature', 'Harmony']
    
    brand_name = f"{random.choice(adjectives)} {random.choice(food_terms)}"
    return brand_name

def generate_nationality():
    """
    Generate a random nationality for a brand.

    Returns:
    - str: The generated nationality.
    """
    nationalities = ['Egyptian', 'American', 'French', 'Italian', 'Spanish', 'Mexican', 'Canadian', 'German', 'Chinese', 'Indian']
    return np.random.choice(nationalities, p=[0.2, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.08])

def generate_brands_insert_statements(num_records):
    """
    Generate INSERT statements for the 'brands' table.

    Parameters:
    - num_records (int): Number of brand records to generate.

    Returns:
    - list: List of INSERT statements for brands.
    """
    insert_statements = []
    brand_id = 1
    for _ in range(num_records):
        name = generate_supermarket_brand_name()
        while name in generated_brand_names:
            name = generate_supermarket_brand_name()
        generated_brand_names.add(name)
        nationality = generate_nationality()
        
        insert_statement = f"INSERT INTO brands (brand_id, name, nationality) VALUES ({brand_id}, '{name}', '{nationality}');"
        insert_statements.append(insert_statement)
        brand_id += 1
    
    return insert_statements

def generate_discount_amount():
    """
    Generate a random discount amount.

    Returns:
    - int: The generated discount amount.
    """
    return random.randint(5, 50)

def generate_discounts_insert_statements(num_records):
    """
    Generate INSERT statements for the 'discounts' table.

    Parameters:
    - num_records (int): Number of discount records to generate.

    Returns:
    - list: List of INSERT statements for discounts.
    """
    insert_statements = []
    discount_id = 1
    called_items=set()

    for _ in range(num_records):
        while True:
            item_id = random.randint(1, N_ITEMS)
            if item_id not in called_items:
                called_items.add(item_id)
                break

        discount_amount = generate_discount_amount()
        start_date = fake.date_between(start_date="-1y", end_date="today")
        end_date = fake.date_between(start_date="today", end_date="+1y")
        
        insert_statement = f"INSERT INTO discounts (discount_id, item_id, discount_amount, start_date, end_date) VALUES ({discount_id}, {item_id}, {discount_amount}, '{start_date}', '{end_date}');"
        insert_statements.append(insert_statement)
        discount_id += 1
        
    return insert_statements

def generate_shopping_carts_insert_statements(num_records):
    """
    Generate INSERT statements for the 'shopping_carts' table.

    Parameters:
    - num_records (int): Number of shopping cart records to generate.

    Returns:
    - list: List of INSERT statements for shopping carts.
    """
    insert_statements = []

    for cart_id in range(1, num_records + 1):
        customer_email = random.choice(tuple(generated_emails))
        creation_time = fake.date_time_this_year()

        insert_statement = f"INSERT INTO shopping_carts (cart_id, customer_email, creation_time) VALUES ({cart_id}, '{customer_email}', '{creation_time}');"
        insert_statements.append(insert_statement)
        generated_carts[cart_id] = creation_time
    
    return insert_statements

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

def generate_promo_code():
    """
    Generate a random alphanumeric promo code.

    Returns:
    - str: The generated promo code.
    """
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))

def generate_discount_amount():
    """
    Generate a random discount amount.

    Returns:
    - int: The generated discount amount.
    """
    return random.randint(10, 100)

def generate_promocodes_insert_statements(num_records):
    """
    Generate INSERT statements for the 'promocodes' table.

    Parameters:
    - num_records (int): Number of promo code records to generate.

    Returns:
    - list: List of INSERT statements for promo codes.
    """
    insert_statements = []

    for _ in range(num_records):
        while True:
            code = generate_promo_code()
            if code not in generated_promocodes:
                generated_promocodes.add(code)
                break
        
        discount_amount = generate_discount_amount()
        start_date = fake.date_between(start_date="-1y", end_date="today")
        end_date = fake.date_between(start_date="today", end_date="+1y")
        
        insert_statement = f"INSERT INTO promocodes (code, discount_amount, start_date, end_date) VALUES ('{code}', {discount_amount}, '{start_date}', '{end_date}');"
        insert_statements.append(insert_statement)
    
    return insert_statements

def generate_payment_promocode_insert_statements(num_records):
    """
    Generate INSERT statements for the 'payment_promocode' table.

    Parameters:
    - num_records (int): Number of payment promo code records to generate.

    Returns:
    - list: List of INSERT statements for payment promo codes.
    """
    insert_statements = []
    called_promocodes = set()

    for _ in range(num_records):
        payment_id = random.randint(1, N_PAYMENTS)
        
        while True:
            code = random.choice(tuple(generated_promocodes))
            if code not in called_promocodes:
                called_promocodes.add(code)
                break
        
        insert_statement = f"INSERT INTO payment_promocode (payment_id, code) VALUES ({payment_id}, '{code}');"
        insert_statements.append(insert_statement)
    
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

def generate_stakeholders_insert_statements():
    """
    Generate INSERT statements for the 'stakeholders' table.

    Returns:
    - list: List of INSERT statements for the 'stakeholders' table.
    """
    insert_statements = []
    called_brands = []
    stakeholder_id = 1

    for _ in range(N_BRANDS):
        brand_id = random.randint(1, N_BRANDS)
        while brand_id in called_brands:
            brand_id = random.randint(1, N_BRANDS)
            
        called_brands.append(brand_id)
        num_stakeholders = random.randint(1, 5)
        remaining_share = 100

        for i in range(num_stakeholders):
            first_name = fake.first_name()
            last_name = fake.last_name()
            nationality = generate_nationality()
            max_share = remaining_share-(num_stakeholders - i - 1)
            
            if i == num_stakeholders-1:
                share = max_share
            else:
                share = random.randint(1, max_share)

            remaining_share -= share
            
            insert_statement = f"INSERT INTO stakeholders (stakeholder_id, first_name, last_name, nationality, share, brand_id) VALUES ({stakeholder_id}, '{first_name}', '{last_name}', '{nationality}', {share}, {brand_id});"
            insert_statements.append(insert_statement)
            stakeholder_id += 1
    
    return insert_statements

def write_queries_to_file(queries, filename):
    """
    Write a list of SQL queries to a text file.

    Parameters:
    - queries (list): List of SQL queries to be written to the file.
    - filename (str): The name of the text file to which the queries will be written.
    """
    with open(filename, 'w') as file:
        for query in queries:
            file.write(query + '\n')

# Generate INSERT statements for each table
customers_insert_queries = generate_customer_insert_statements(N_CUSTOMERS)
brands_insert_queries = generate_brands_insert_statements(N_BRANDS)
items_insert_queries = generate_items_insert_statements(N_ITEMS)
promocodes_insert_queries = generate_promocodes_insert_statements(N_PROMOCODES)
shopping_carts_insert_queries = generate_shopping_carts_insert_statements(N_CARTS)
discounts_insert_queries = generate_discounts_insert_statements(N_DISCOUNTS)
cart_item_insert_queries = generate_cart_item_insert_statements(N_CART_ITEMS)
payments_insert_queries = generate_payments_insert_statements(N_PAYMENTS)
payment_promocode_insert_queries = generate_payment_promocode_insert_statements(N_PAYMENT_PROMOCODE)
stakeholders_insert_queries = generate_stakeholders_insert_statements()

# Combine all queries into a single list
all_queries = (
    customers_insert_queries +
    brands_insert_queries +
    items_insert_queries +
    promocodes_insert_queries +
    shopping_carts_insert_queries +
    discounts_insert_queries +
    cart_item_insert_queries +
    payments_insert_queries +
    payment_promocode_insert_queries+
    stakeholders_insert_queries
)

# Write queries to text files
write_queries_to_file(customers_insert_queries, 'customers_insert_queries.txt')
print("Customers Insert Queries Done")
write_queries_to_file(brands_insert_queries, 'brands_insert_queries.txt')
print("Brands Insert Queries Done")
write_queries_to_file(items_insert_queries, 'items_insert_queries.txt')
print("Items Insert Queries Done")
write_queries_to_file(promocodes_insert_queries, 'promocodes_insert_queries.txt')
print("Promocodes Insert Queries Done")
write_queries_to_file(shopping_carts_insert_queries, 'shopping_carts_insert_queries.txt')
print("Shopping Carts Insert Queries Done")
write_queries_to_file(discounts_insert_queries, 'discounts_insert_queries.txt')
print("Discounts Insert Queries Done")
write_queries_to_file(cart_item_insert_queries, 'cart_item_insert_queries.txt')
print("Cart Items Insert Queries Done")
write_queries_to_file(payments_insert_queries, 'payments_insert_queries.txt')
print("Payments Insert Queries Done")
write_queries_to_file(payment_promocode_insert_queries, 'payment_promocode_insert_queries.txt')
print("Payment Promocode Insert Queries Done")
write_queries_to_file(stakeholders_insert_queries, 'stakeholders_insert_queries.txt')
print("Stakeholders Insert Queries Done")
write_queries_to_file(all_queries, 'all_insert_queries.txt')
print("All Insert Queries Done")