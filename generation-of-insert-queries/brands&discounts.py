import random
from faker import Faker
import numpy as np

N_ITEMS = 50
N_BRANDS = 20
N_DISCOUNTS = 20

fake = Faker()

# Function to create realistic brand names for a supermarket
def generate_supermarket_brand_name():
    # List of adjectives to pair with a food-related term for a brand name
    adjectives = ['Golden', 'Fresh', 'Pure', 'Organic', 'Natural', 'Tasty', 'Quality', 'Premium', 'Classic']
    # List of food-related terms
    food_terms = ['Harvest', 'Fields', 'Gardens', 'Orchard', 'Market', 'Kitchen', 'Delights', 'Farms', 'Bounty']
    
    # Select a random adjective and a food term to create a brand name
    brand_name = f"{random.choice(adjectives)} {random.choice(food_terms)}"
    return brand_name

# Function to generate nationalities
def generate_nationality():
    # Some possible nationalities for diversity in brand origins
    nationalities = ['Egyptian', 'American', 'French', 'Italian', 'Spanish', 'Mexican', 'Canadian', 'German', 'Chinese', 'Indian']
    return np.random.choice(nationalities, p=[0.2, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.08])

# Function to create insert statements for the 'brands' table

def generate_brands_insert_statements(num_records):
    insert_statements = []
    brand_id = 1
    for _ in range(num_records):
        name = generate_supermarket_brand_name()
        nationality = generate_nationality()
        
        # Construct the insert statement
        insert_statement = f"INSERT INTO brands (id, name, nationality) VALUES ({brand_id}, '{name}', '{nationality}');"
        insert_statements.append(insert_statement)
        brand_id += 1
    
    return insert_statements

# Function to generate random discount amounts
def generate_discount_amount():
    # Generate a random discount amount between 5% and 50%
    return random.randint(5, 50)

# Function to create insert statements for the 'discounts' table

def generate_discounts_insert_statements(num_records):
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
        
        # Construct the insert statement
        insert_statement = f"INSERT INTO discounts (discount_id, item_id, discount_amount, start_date, end_date) VALUES ({discount_id}, {item_id}, {discount_amount}, '{start_date}', '{end_date}');"
        insert_statements.append(insert_statement)
        discount_id += 1
        
    return insert_statements