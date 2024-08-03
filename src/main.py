from fastapi import FastAPI
from handlers import  user, admin
import model 
from database import engine 

app = FastAPI()
app.include_router(user)
app.include_router(admin)




model.Base.metadata.create_all(engine)


