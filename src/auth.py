from datetime import timedelta, datetime 
from typing import Annotated
from passlib.context import CryptContext 
from jose import jwt, JWTError 
from fastapi import HTTPException, Depends
from starlette import status 
from fastapi.security import OAuth2PasswordBearer 
from pydantic import BaseModel
from config import config

from database.user import Users 
from database.admin import Admin

SECRET_KEY = config.SECRET_KEY 
ALGORITHM = config.ALGORITHM

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
user_oauth2_bearer = OAuth2PasswordBearer(tokenUrl='user/token')
admin_oauth2_bearer = OAuth2PasswordBearer(tokenUrl='admin/token')

class Token(BaseModel):
    access_token: str
    token_type: str 


def create_user(username: str , password: str, role: str): 
    if role == "users":
        user = Users(
            username=username,
            hashed_password=bcrypt_context.hash(password)
        )
        return user 
    elif role == "admin":
        admin = Admin(
                username=username,
                hashed_password=bcrypt_context.hash(password)
        )
        return admin 
    else:
        return None 

def authenticate_user(username: str, password: str, db):
    
    user = db.query(Users).filter(Users.username == username).first() 

    if not user:
        return False 
    if not bcrypt_context.verify(password, user.hashed_password):
        return False 
    return user 

def authenticate_admin(username: str, password: str,db):
    admin = db.query(Admin).filter(Admin.username == username).first() 

    if not admin:
        return False
    if not bcrypt_context.verify(password, admin.hashed_password):
        return False 
    return admin 
    

def create_access_token(username: str, user_id: int,  exp: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + exp
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(user_oauth2_bearer)]):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
       
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")


async def get_current_admin(token: Annotated[str, Depends(admin_oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user") 
