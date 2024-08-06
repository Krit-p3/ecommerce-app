from fastapi import APIRouter
from starlette import status

from typing import List
from database.product import Products
from schema.product import Product, CreateProduct, UpdateProduct
from lib import db_dependency, admin_dependency
from service.product import add_product, update_product, delete_product, search_product

product = APIRouter(prefix="/product", tags=["product"])


@product.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateProduct)
async def create(product: CreateProduct, db: db_dependency, admin: admin_dependency):
    _product = Products(**product.dict())
    res = add_product(_product, db)
    return res


@product.patch("/{product_id}", response_model=Product)
async def update(
    product_id: int, product: UpdateProduct, db: db_dependency, admin: admin_dependency
):
    res = update_product(product_id, product, db)
    return res


@product.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(product_id: int, db: db_dependency, admin: admin_dependency):
    res = delete_product(product_id, db)
    return res


@product.get("/", response_model=List[Product])
async def get_products(db: db_dependency, admin: admin_dependency):
    products = db.query(Products).all()
    return products


@product.get("/{product_name}", response_model=Product)
async def get_product(product_name: str, db: db_dependency, admin: admin_dependency):
    res = search_product(product_name, db)
    return res
