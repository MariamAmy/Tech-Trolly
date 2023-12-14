import random
from faker import Faker

N_PAYMENTS = 50
N_PROMOCODES = 20
N_PAYMENT_PROMOCODE = int(0.2*N_PAYMENTS)
generated_promocodes = []

# Instantiate a Faker object
fake = Faker()

# Function to create insert statements for the 'payment_promocode' table
def generate_payment_promocode_insert_statements(num_records):
    insert_statements = []
    called_promocodes = set()

    for _ in range(num_records):
        # Ensure we use each payment ID only once
        payment_id = random.randint(1, N_PAYMENTS)
        
        # Generate a promo code that is assumed to be a valid code from the promocodes table
        while True:
            code = random.choice(generated_promocodes)
            if code not in called_promocodes:
                called_promocodes.add(code)
                break
        
        # Construct the insert statement
        insert_statement = f"INSERT INTO payment_promocode (payment_id, code) VALUES ({payment_id}, '{code}');"
        insert_statements.append(insert_statement)
    
    return insert_statements

# Function to generate a random alphanumeric code for the promo code
def generate_promo_code():
    # Generate a random alphanumeric code of length 6
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))

# Function to generate random discount amounts
def generate_discount_amount():
    # Generate a random discount amount between 10 and 100
    return random.randint(10, 100)

# Function to create insert statements for the 'promocodes' table
def generate_promocodes_insert_statements(num_records):
    insert_statements = []
    called_promocodes = set()

    for _ in range(num_records):
        while True:
            code = generate_promo_code()
            if code not in called_promocodes:
                called_promocodes.add(code)
                break
        
        generated_promocodes.append(code)
        discount_amount = generate_discount_amount()
        start_date = fake.date_between(start_date="-1y", end_date="today")
        end_date = fake.date_between(start_date="today", end_date="+1y")
        
        # Construct the insert statement
        insert_statement = f"INSERT INTO promocodes (code, discount_amount, start_date, end_date) VALUES ('{code}', {discount_amount}, '{start_date}', '{end_date}');"
        insert_statements.append(insert_statement)
    
    return insert_statements