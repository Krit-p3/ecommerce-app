from fastapi import FastAPI
from route import user, admin, product, orders
from database.db import engine, Base


app = FastAPI()
app.include_router(user)
app.include_router(admin)
app.include_router(product)
app.include_router(orders)


Base.metadata.create_all(engine)
