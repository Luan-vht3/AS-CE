import random
import time
import datetime as dt
import pandas as pd
import multiprocessing as mp
from collections import deque
from initial_data import generate_initial_data
from city_graph import generate_city_graph
from entities import Consumer, Store, Product, Budget
from dataclasses import dataclass
from faker import Faker
import networkx as nx
import csv

fake = Faker()

@dataclass
class Order:
    consumer_id: int
    store_id: int
    product_id: int
    quantity: int


class Simulator:
    def __init__(self,
            duration: int = 15,
            num_orders_per_cycle: int = 300,
            num_consumers: int = 200,
            num_stores: int = 10,
            num_products: int = 20,
            num_neighborhoods: int = 20
        ):
        self.duration = duration
        self.cycle = 0
        self.num_orders_per_cycle = num_orders_per_cycle

        self.orders = deque()
        self.budgets = deque()
        self.approved_budgets = deque()
        self.rejected_budgets = deque()
        
        self.neighborhoods = [fake.city() for _ in range(num_neighborhoods)]
        self.consumers, self.stores, self.products = generate_initial_data(
            num_consumers=num_consumers,
            num_stores=num_stores,
            num_products=num_products,
            neighborhoods=self.neighborhoods
        )
        self.city_graph = generate_city_graph(self.neighborhoods)
        self.load_data()

    def load_data(self):
        self.consumers = pd.read_csv('src/data/consumers.csv').to_dict(orient='records')
        self.stores = pd.read_csv('src/data/stores.csv').to_dict(orient='records')
        self.products = pd.read_csv('src/data/products.csv').to_dict(orient='records')
    
    def update_stocks(self):
        for product in self.products:
            if random.random() > 0.2: continue
            product['stock_quantity'] += 20
            if product['stock_quantity'] > 2000:
                product['stock_quantity'] = 2000
    
    def create_order(self, consumer_id: int) -> Order:
        store = random.choice(self.stores)
        product = random.choice(self.products)
        N = int(1 / random.uniform(0.002, 1)) # Higher chance of choosing smaller quantities
        order = Order(
            consumer_id=consumer_id,
            store_id=store['id'],
            product_id=product['id'],
            quantity=N,
        )
        self.orders.append(order)
        return order
    
    def create_budget(self, order: Order, creation_date: str) -> Budget:
        # Get the consumer, product, and store
        consumer = self.consumers[order.consumer_id - 1]
        product = self.products[order.product_id - 1]
        store = self.stores[order.store_id - 1]

        # Calculate the budget price
        base_price = product['price'] * order.quantity
        distance = nx.shortest_path_length(self.city_graph, consumer['neighborhood'], store['neighborhood'])
        shipping_price = product['weight'] * order.quantity * store['weight_rate'] * distance
        total_price = round(base_price + shipping_price, 2)
        
        # Create the budget
        budget = Budget(
            id=len(self.budgets) + 1,
            creation_date=creation_date,
            consumer_id=order.consumer_id,
            store_id=order.store_id,
            product_id=order.product_id,
            quantity=order.quantity,
            state='created',
            price=total_price
        )
        self.budgets.append(budget)
        return budget

    def confirm_budget(self, order: Order, budget: Budget):
        product = self.products[order.product_id - 1]
        if product['stock_quantity'] >= order.quantity:
            product['stock_quantity'] -= order.quantity
            budget.state = 'approved' if random.random() < 0.5 else 'rejected'
        else:
            budget.state = 'rejected'

    def process_order(self, consumer_id: int):
        order = self.create_order(consumer_id)
        #with lock:
        self.log_orders(order)
        
        time.sleep(random.uniform(0.001, 0.01))
        
        creation_date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        budget = self.create_budget(order, creation_date)
        #with lock:
        self.log_budgets(budget)
        time.sleep(random.uniform(0.001, 0.01))

        self.confirm_budget(order, budget)
        time.sleep(random.uniform(0.001, 0.01))

        if budget.state == 'approved':
            self.approved_budgets.append(budget)
        elif budget.state == 'rejected':
            self.rejected_budgets.append(budget)
        
        #with lock:
        self.log_budgets(budget)

    
    def run(self) -> None:
        END = time.time() + self.duration
        while time.time() < END:
            self.cycle += 1
            print(f"Cycle {self.cycle}")

            with mp.Pool(mp.cpu_count()) as pool:
                pool.map(
                    self.process_order,
                    [random.randint(1, len(self.consumers)) for _ in range(self.num_orders_per_cycle)]
                )

            if self.cycle % 10 == 0:
                self.update_stocks()
        
        print("Simulation finished.")


    def log_orders(self, order: Order) -> None:
        with open('src/data/orders.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                order.consumer_id,
                order.store_id,
                order.product_id,
                order.quantity,
                dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            ])

    def log_budgets(self, budget: Budget) -> None:
        with open('src/data/budgets.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                budget.id,
                budget.creation_date,
                budget.consumer_id,
                budget.store_id,
                budget.product_id,
                budget.quantity,
                budget.state,
                budget.price,
                dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            ])

# Main function to run the simulation
if __name__ == "__main__":
    NUM_NEIGHBORHOODS = 20
    NUM_CONSUMERS = 200
    NUM_STORES = 10
    NUM_PRODUCTS = 20
    
    simulator = Simulator(
        duration=15,
        num_consumers=NUM_CONSUMERS,
        num_stores=NUM_STORES,
        num_products=NUM_PRODUCTS,
        num_neighborhoods=NUM_NEIGHBORHOODS
    )
    
    simulator.run()
