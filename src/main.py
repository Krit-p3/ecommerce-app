from fastapi import FastAPI
from route import user, admin, product
 
from database.db import engine, Base 

app = FastAPI()
app.include_router(user)
app.include_router(admin)
app.include_router(product)




Base.metadata.create_all(engine)


