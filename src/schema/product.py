from pydantic import BaseModel

class Product(BaseModel):
    id: int 
    name: str 
    description: str 
    price: float
    size: str 
    quantity: float

class CreateProduct(BaseModel):
    name: str 
    description: str
    price: float 
    size: str
    quantity: float


