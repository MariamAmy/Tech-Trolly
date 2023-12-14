import random
import hashlib
from faker import Faker

generated_emails = []

# Instantiate a Faker object
fake = Faker()

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Function to generate phone numbers
def generate_phone_number():
    # Egyptian phone numbers start with +2010, +2011, +2012, or +2015
    prefixes = ['+2010', '+2011', '+2012', '+2015']
    # Choose a random prefix and generate the rest of the number (total length should be 13 including the prefix)
    return random.choice(prefixes) + ''.join(random.choice('0123456789') for _ in range(8))

# Function to create insert statements for the 'customers' table
def generate_customer_insert_statements(num_records):
    insert_statements = []
    
    for _ in range(num_records):
        email = fake.email()
        generated_emails.append(email)
        password = hash_password(fake.password(length=12))
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone_number = generate_phone_number()
        
        # Construct the insert statement
        insert_statement = f"INSERT INTO customers (email, password, first_name, last_name, phone_number) VALUES ('{email}', '{password}', '{first_name}', '{last_name}', '{phone_number}');"
        insert_statements.append(insert_statement)
    
    return insert_statements

def generate_shopping_carts_insert_statements(num_records):
    insert_statements = []

    for cart_id in range(1, num_records + 1):
        customer_email = random.choice(generated_emails)    
        creation_time = fake.date_time_this_year()  # Generate a random datetime from this year

        # Construct the insert statement
        insert_statement = f"INSERT INTO shopping_carts (cart_id, customer_email, creation_time) VALUES ({cart_id}, '{customer_email}', '{creation_time}');"
        insert_statements.append(insert_statement)
    
    return insert_statements
