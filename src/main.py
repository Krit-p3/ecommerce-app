from fastapi import FastAPI
from route import user, admin
 
from database.db import engine, Base 

app = FastAPI()
app.include_router(user)
app.include_router(admin)




Base.metadata.create_all(engine)


