import os
import random
import pandas as pd
from faker import Faker
from entities import Consumer, Store, Product
import shutil

fake = Faker()

def generate_initial_data(
        num_consumers: int,
        num_stores: int,
        num_products: int,
        neighborhoods: list[str]
    ) -> tuple[list[Consumer], list[Store], list[Product]]:
    consumers = []
    for i in range(1, num_consumers + 1):
        consumer = Consumer(
            id=i,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            dob=fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d"),
            neighborhood=random.choice(neighborhoods)
        )
        consumers.append(consumer)

    stores = []
    for i in range(1, num_stores + 1):
        store = Store(
            id=i,
            cnpj=fake.ssn(),
            name=fake.company(),
            neighborhood=random.choice(neighborhoods),
            weight_rate=random.uniform(0.1, 0.5)
        )
        stores.append(store)

    products = []
    for i in range(1, num_products + 1):
        product = Product(
            id=i,
            name=fake.word(),
            price=random.uniform(10, 100),
            weight=random.uniform(0.5, 5),
            stock_quantity=100
        )
        products.append(product)

    # Convert to DataFrames for easier manipulation
    consumers_df = pd.DataFrame([consumer.__dict__ for consumer in consumers])
    stores_df = pd.DataFrame([store.__dict__ for store in stores])
    products_df = pd.DataFrame([product.__dict__ for product in products])

    # Remove existing data folder and create a new one
    if os.path.exists('src/data'): shutil.rmtree('src/data')
    os.makedirs('src/data')

    # Save to CSV
    consumers_df.to_csv('src/data/consumers.csv', index=False)
    stores_df.to_csv('src/data/stores.csv', index=False)
    products_df.to_csv('src/data/products.csv', index=False)

    print("Data generation complete. Consumers, stores, and products saved to CSV.")

    return consumers, stores, products

if __name__ == "__main__":
    generate_initial_data(100, 10, 20, ["Neighborhood 1", "Neighborhood 2", "Neighborhood 3"])
