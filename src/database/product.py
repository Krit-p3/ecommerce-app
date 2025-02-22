from .db import Base
from sqlalchemy import Column, Integer, String, Float


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Float)
    size = Column(String)
    quantity = Column(Float)
