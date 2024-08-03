from fastapi import APIRouter, Depends, HTTPException 
from starlette import status 
from datetime import timedelta
import auth
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from schema.user import ClientRequest 
from lib import db_dependency, admin_dependency


product = APIRouter(prefix="/product", tags=["product"])

async def create_product():
    pass 


async def update_product():
    pass 

async def delete_product():
    pass 

async def get_product():
    pass 

async def get_products():
    pass 

