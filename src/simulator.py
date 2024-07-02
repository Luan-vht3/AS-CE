import random
import time
import pandas as pd
import multiprocessing as mp
import requests
from initial_data import generate_initial_data
from city_graph import generate_city_graph
from entities import Consumer, Store, Product
from dataclasses import dataclass
from faker import Faker

NUM_NEIGHBORHOODS = 20
NUM_CONSUMERS = 200
NUM_STORES = 10
NUM_PRODUCTS = 20
NUM_PROCESSES = 4

fake = Faker()

"""
A aplicação de simulação deverá representar múltiplos consumidores interagindo
com o sistema executando a seguinte rotina:
1. Escolher uma loja dentre as disponíveis.
2. Criar um pedido composto por N unidades de um produto ofertado pela loja.
   - O produto deve estar disponível em estoque.
3. Solicitar o orçamento para o pedido
   - O cálculo do orçamento é:
     base price == product price * quantity
     shipping price == product weight * quantity * store weight rate * distance from consumer neighborhood to store neighborhood
     total price == base price + shipping price
4. Opcionalmente confirmar o orçamento
   - O consumidor deverá aceitar 50% dos orçamentos.
   - A loja deverá aceitar o orçamento caso tenha os produtos em estoque, caso contrário o mesmo deverá ser cancelado

"""

@dataclass
class Order:
    consumer_id: int
    store_id: int
    product_id: int
    quantity: int


class Simulator:
    def __init__(self):
        self.lock = mp.Lock()
        self.neighborhoods = [fake.city() for _ in range(NUM_NEIGHBORHOODS)]
        self.consumers, self.stores, self.products = generate_initial_data(
            NUM_CONSUMERS, NUM_STORES, NUM_PRODUCTS, self.neighborhoods
        )
        self.city_graph = generate_city_graph(self.neighborhoods)
        self.load_data()

    def load_data(self):
        self.consumers = pd.read_csv('src/data/consumers.csv').to_dict(orient='records')
        self.stores = pd.read_csv('src/data/stores.csv').to_dict(orient='records')
        self.products = pd.read_csv('src/data/products.csv').to_dict(orient='records')

    def choose_store(self):
        return random.choice(self.stores)
    
    def choose_product(self):
        # We'll check stock availability later
        return random.choice(self.products)
    
    def create_order(self, consumer_id):
        store = self.choose_store()
        product = self.choose_product()
        N = random.randint(1, product['stock_quantity'])
        return Order(
            consumer_id=consumer_id,
            store_id=store['id'],
            product_id=product['id'],
            quantity=N,
        )
    
    def calculate_distance(self, order):
        consumer = self.consumers[order.consumer_id - 1]
        store = self.stores[order.store_id - 1]
        return self.city_graph.shortest_path_length(consumer['neighborhood'], store['neighborhood'])
    
    def request_quote(self, order):
        consumer = self.consumers[order.consumer_id - 1]
        store = self.stores[order.store_id - 1]
        product = self.products[order.product_id - 1]
        distance = 1


    def run_simulation(self):
        start = time.time()
        ...
        end = time.time()
        #print(f"Simulation finished in {end - start:.2f} seconds.")
    


# Main function to run the simulation
if __name__ == "__main__":
    simulator = Simulator()
    
    #simulator.run_simulation()
