from dataclasses import dataclass

@dataclass
class Consumer:
    id: int
    first_name: str
    last_name: str
    dob: str
    neighborhood: str

@dataclass
class Product:
    id: int
    name: str
    price: float
    weight: float
    stock_quantity: int  # quantity available in stock for all stores added together

@dataclass
class Store:
    id: int
    cnpj: str
    name: str
    neighborhood: str
    weight_rate: float

@dataclass
class Budget:
    id: int
    creation_date: str # "YYYY-MM-DD HH:MM:SS"
    consumer_id: int
    store_id: int
    product_id: int
    quantity: int
    state: str  # "created", "pending", "approved", "rejected", or "canceled".
    price: float

# base price == product price * quantity
# shipping price == product weight * quantity * store weight rate * distance from consumer neighborhood to store neighborhood
# total price == base price + shipping price

# total_price == product.price * quantity + product.weight * quantity * store.weight_rate * distance
