from database.product import Products 
from starlette import status 
from fastapi import HTTPException

def add_product(product: Products, db):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product 

def update_product(product_id: int, product: Products, db):
    _product = db.query(Products).filter(Products.id == product_id).first() 
    
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    for k,v in product.dict().items():
        setattr(_product, k, v)

    db.commit()
    db.refresh(_product)
    return _product

def delete_product(product_id: int, db):

    product = db.query(Products).filter(Products.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(product)
    db.commit()
    return None 

def search_product(product_name, db):
    product = db.query(Products).filter(Products.name == product_name).first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product 
