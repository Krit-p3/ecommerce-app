from database import Base 
from sqlalchemy import Column, Integer, String 
from pydantic import BaseModel 



class Users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

class ClientRequest(BaseModel):
    username: str 
    password: str 

class Admin(Base):
    __tablename__ = "Admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)


