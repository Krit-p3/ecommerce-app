from fastapi import APIRouter, Depends, HTTPException
from starlette import status
import auth
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from schema.user import ClientRequest
from lib import db_dependency, admin_dependency
from service.admin import register_admin, is_valid_admin


admin = APIRouter(prefix="/admin", tags=["admin"])


@admin.post("/", status_code=status.HTTP_201_CREATED)
async def create_admin(request: ClientRequest, db: db_dependency):
    res = register_admin(request.username, request.password, db)
    return res


@admin.post("/token", response_model=auth.Token)
async def admin_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    res = is_valid_admin(form_data.username, form_data.password, db)
    return res


@admin.get("/", status_code=status.HTTP_200_OK)
async def _admin(admin: admin_dependency, db: db_dependency):
    if admin is None:
        raise HTTPException(status_code=401, details="Authentication failed")
    return {"User": admin}
