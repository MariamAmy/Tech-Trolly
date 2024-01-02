import random
from faker import Faker

# Constants
N_BRANDS = 100

# Sets to keep track of generated data
generated_brand_names = set()

# Instantiate a Faker object
fake = Faker()

def generate_nationality():
    """
    Generate a random nationality for a brand.

    Returns:
    - str: The generated nationality.
    """
    nationalities = ['Egyptian', 'American', 'French', 'Italian', 'Spanish', 'Mexican', 'Canadian', 'German', 'Chinese', 'Indian']
    return random.choice(nationalities)

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

# Generate INSERT statements for the 'stakeholders' table
stakeholders_insert_queries = generate_stakeholders_insert_statements()