import random
import hashlib
import numpy as np
from faker import Faker

# Constants
N_ITEMS = 1000
N_BRANDS = 100
N_DISCOUNTS = 200

# Sets to keep track of generated data
generated_brand_names = set()

# Instantiate a Faker object
fake = Faker()

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
    called_items = set()

    for _ in range(num_records):
        while True:
            item_id = random.randint(1, N_ITEMS)  # Assuming N_ITEMS is defined somewhere
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

# Generate INSERT statements for the 'brands' table
brands_insert_queries = generate_brands_insert_statements(N_BRANDS)

# Generate INSERT statements for the 'discounts' table
discounts_insert_queries = generate_discounts_insert_statements(N_DISCOUNTS)
