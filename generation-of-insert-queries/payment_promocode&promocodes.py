import random
from faker import Faker
from datetime import timedelta

# Constants
N_PAYMENTS = 110
N_PROMOCODES = 50
N_PAYMENT_PROMOCODE = int(0.2 * N_PAYMENTS)

# Sets to keep track of generated data
generated_promocodes = set()

# Instantiate a Faker object
fake = Faker()

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

# Generate INSERT statements for the 'payment_promocode' table
payment_promocode_insert_queries = generate_payment_promocode_insert_statements(N_PAYMENT_PROMOCODE)

# Generate INSERT statements for the 'promocodes' table
promocodes_insert_queries = generate_promocodes_insert_statements(N_PROMOCODES)