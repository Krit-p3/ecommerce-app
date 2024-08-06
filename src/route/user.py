from fastapi import APIRouter, Depends, HTTPException
from starlette import status
import auth
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from schema.user import ClientRequest
from lib import db_dependency, user_dependency
from service.user import register_user, is_valid_user

user = APIRouter(prefix="/user", tags=["user"])


@user.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: ClientRequest, db: db_dependency):
    res = register_user(request.username, request.password, db)
    return res


@user.post("/token", response_model=auth.Token)
async def user_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    res = is_valid_user(form_data.username, form_data.password, db)
    return res


@user.get("/", status_code=status.HTTP_200_OK)
async def _user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, details="Authentication failed")
    return {"User": user}
