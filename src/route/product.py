from fastapi import APIRouter, HTTPException 
from starlette import status 

from typing import  List
from database.product import Products
from schema.product import Product, CreateProduct
from lib import db_dependency, admin_dependency


product = APIRouter(prefix="/product", tags=["product"])

@product.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateProduct)
async def create_product(product: CreateProduct,db: db_dependency, admin: admin_dependency):
    _product = Products(**product.dict())
    db.add(_product)
    db.commit()
    db.refresh(_product)
    return _product 

@product.patch("/{product_id}", response_model=Product)
async def update_product(product_id: int , product: Product, db: db_dependency, admin: admin_dependency):
    _product = db.query(Products).filter(Products.id == product_id).first()
    if _product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    for k,v in product.dict().items():
        setattr(_product,k,v)

    db.commit()
    db.refresh(_product)
    return _product
    
 

@product.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: db_dependency, admin: admin_dependency):
    _product = db.query(Products).filter(Products.id == product_id).first()
    if _product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(_product)
    db.commit()
    return None # will chaneg to HTTP Response 

@product.get("/", response_model=List[Product])
async def get_product(db: db_dependency, admin: admin_dependency):
    products = db.query(Products).all()
    return products
    

@product.get("/{product_name}", response_model=Product)
async def get_products(product_name: str ,db: db_dependency, admin: admin_dependency):
    _product = db.query(Products).filter(Products.name == product_name).first() 
    
    if _product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return _product
    

