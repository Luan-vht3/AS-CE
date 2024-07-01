from dataclasses import dataclass

@dataclass
class Consumer:
    id: int
    first_name: str
    last_name: str
    dob: str
    neighborhood: str

@dataclass
class Store:
    id: int
    cnpj: str
    name: str
    neighborhood: str
    weight_rate: float

@dataclass
class Product:
    id: int
    name: str
    price: float
    weight: float
    stock_quantity: int

@dataclass
class Quote:
    id: int
    creation_date: str
    consumer_id: int
    store_id: int
    product_id: int
    quantity: int
    state: str  # "created", "pending", "approved", "rejected", or "canceled".
    price: float

