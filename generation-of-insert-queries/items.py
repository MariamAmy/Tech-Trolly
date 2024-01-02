import random
from faker import Faker

# Constants
N_ITEMS = 1000
N_BRANDS = 100

# Sets to keep track of generated data
generated_brand_names = set()

# Instantiate a Faker object
fake = Faker()

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

# Generate INSERT statements for the 'items' table
items_insert_queries = generate_items_insert_statements(N_ITEMS)