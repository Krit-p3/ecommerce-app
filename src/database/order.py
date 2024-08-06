from .db import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    total_amount = Column(Float)
    create_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("OrderItems", back_populates="order")


class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.order_id"))
    product_id = Column(String, index=True)
    quantity = Column(Integer)
    order = relationship("Orders", back_populates="items")
