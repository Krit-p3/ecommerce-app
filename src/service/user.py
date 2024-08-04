import auth 
from fastapi import HTTPException 
from starlette import status 
from datetime import timedelta

def is_valid_user(username: str, password: str, db):

    user = auth.authenticate_user(username, password,db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could't validate user")
    token = auth.create_access_token(user.username, user.id, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer'}

def register_user(username: str, password: str, db):
    user = auth.create_user(username, password, "users")

    db.add(user)
    db.commit()
    return {"User created."}


