from fastapi import APIRouter, Depends, HTTPException 
from starlette import status 
from datetime import timedelta
import auth
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from schema.user import ClientRequest 
from lib import db_dependency, user_dependency

user = APIRouter(prefix='/user', tags=['user'])

@user.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(request: ClientRequest, db: db_dependency):
    user = auth.create_user(request.username, request.password, "users")

    db.add(user)
    db.commit()



@user.post('/token', response_model=auth.Token)
async def user_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
     
    user = auth.authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could't validate user")
    token = auth.create_access_token(user.username, user.id, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer'}

@user.get("/", status_code=status.HTTP_200_OK)
async def _user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, details="Authentication failed")
    return {"User": user}

