import random
from faker import Faker
import numpy as np

# Instantiate a Faker object
fake = Faker()

def generate_nationality():
    # Some possible nationalities for diversity in brand origins
    nationalities = ['Egyptian', 'American', 'French', 'Italian', 'Spanish', 'Mexican', 'Canadian', 'German', 'Chinese', 'Indian']
    return np.random.choice(nationalities, p=[0.2, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.08])

# Function to create insert statements for the 'customers' table
def generate_customer_insert_statements():
    insert_statements = []
    called_brands = []
    stakeholder_id = 1
    for _ in range(20):
        brand_id = random.randint(1, 20)
        while brand_id in called_brands:
            brand_id = random.randint(1, 20)
            
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
            
            # Construct the insert statement
            insert_statement = f"INSERT INTO stakeholders (stakeholder_id, first_name, last_name, nationality, share, brand_id) VALUES ({stakeholder_id}, '{first_name}', '{last_name}', '{nationality}', {share}, {brand_id});"
            insert_statements.append(insert_statement)
            stakeholder_id += 1
    
    return insert_statements

for i in generate_customer_insert_statements():
    print(i)