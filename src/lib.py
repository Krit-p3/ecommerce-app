from database.db import SessionLocal 
from typing import Annotated 
from fastapi import Depends 
from sqlalchemy.orm import Session 
from auth import get_current_user, get_current_admin


def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[Session, Depends(get_current_user)]

admin_dependency = Annotated[Session, Depends(get_current_admin)]
