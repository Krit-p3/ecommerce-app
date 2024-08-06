from pydantic import BaseModel
from typing import List


class CartItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int


class Order(BaseModel):
    user_id: str
    order_id: str
    items: List[CartItem]


class Payment(BaseModel):
    order_id: str
    amount: float
