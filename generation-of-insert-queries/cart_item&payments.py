import random
from faker import Faker

N_CARTS = 60
N_CART_ITEMS = 500
N_ITEMS = 50

# Instantiate a Faker object
fake = Faker()

# Function to create insert statements for the 'payment_promocode' table
def generate_cart_item_insert_statements(num_records):
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
        
        # Construct the insert statement
        insert_statement = f"INSERT INTO cart_item (cart_id, item_id, quantity) VALUES ({cart_id}, {item_id}, {quantity});"
        insert_statements.append(insert_statement)
    
    return insert_statements
