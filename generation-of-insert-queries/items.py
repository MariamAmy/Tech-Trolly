import random
from faker import Faker

N_BRANDS = 20
N_ITEMS = 50

fake = Faker()

def generate_expiration_date():
    # Generate a date between 1 and 5 years from now
    return fake.date_between(start_date="today", end_date="+5y")

# Function to create more realistic item names for a supermarket
def generate_supermarket_item_name():
    # List of possible item categories
    categories = ['Dairy', 'Bakery', 'Beverages', 'Snacks', 'Meat', 'Seafood', 'Produce', 'Canned Goods', 'Frozen Food', 'Personal Care']
    # List of possible item types within categories
    item_types = {
        'Dairy': ['Milk', 'Cheese', 'Yogurt', 'Butter', 'Cream'],
        'Bakery': ['Bread', 'Cookies', 'Cake', 'Muffins', 'Pies'],
        'Beverages': ['Juice', 'Soda', 'Water', 'Tea', 'Coffee'],
        'Snacks': ['Chips', 'Nuts', 'Candy', 'Chocolate', 'Popcorn'],
        'Meat': ['Chicken', 'Beef', 'Pork', 'Lamb', 'Turkey'],
        'Seafood': ['Fish', 'Shrimp', 'Crab', 'Lobster', 'Oysters'],
        'Produce': ['Apples', 'Bananas', 'Tomatoes', 'Lettuce', 'Carrots'],
        'Canned Goods': ['Beans', 'Soup', 'Corn', 'Peas', 'Tomato Sauce'],
        'Frozen Food': ['Pizza', 'Dumplings', 'Ice Cream', 'Berries', 'Vegetables'],
        'Personal Care': ['Soap', 'Shampoo', 'Toothpaste', 'Lotion', 'Deodorant']
    }
    
    # Select a random category
    category = random.choice(categories)
    # Select a random item type within the selected category
    item_name = random.choice(item_types[category])
    
    return f"{category} {item_name}"

# Update the function to generate items insert statements with realistic item names

def generate_realistic_items_insert_statements(num_records):
    item_id = 1
    insert_statements = []
    
    for _ in range(num_records):
        name = generate_supermarket_item_name()
        quantity = random.randint(1, 100)  # Random quantity between 1 and 100
        price = round(random.uniform(0.5, 100.0), 2)  # Random price between 0.5 and 100.0, rounded to 2 decimal places
        brand_id = random.randint(1, N_BRANDS)  # Assuming there are 10 brands available
        expiry_date = generate_expiration_date()
        
        # Construct the insert statement
        insert_statement = f"INSERT INTO items (item_id, name, quantity, price, brand_id, expiry_date) VALUES ({item_id}, '{name}', {quantity}, {price}, {brand_id}, '{expiry_date}');"
        insert_statements.append(insert_statement)
        item_id += 1
    return insert_statements