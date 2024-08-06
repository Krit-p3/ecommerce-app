from .db import Base
from sqlalchemy import Column, Integer, String


class Admin(Base):
    __tablename__ = "Admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
