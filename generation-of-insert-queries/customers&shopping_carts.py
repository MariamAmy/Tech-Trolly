import random
import hashlib
import numpy as np
from faker import Faker

# Constants
N_CUSTOMERS = 100
N_CARTS = 120

# Sets to keep track of generated data
generated_emails = set()
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

# Generate INSERT statements for the 'customers' table
customers_insert_queries = generate_customer_insert_statements(N_CUSTOMERS)

# Generate INSERT statements for the 'shopping_carts' table
shopping_carts_insert_queries = generate_shopping_carts_insert_statements(N_CARTS)