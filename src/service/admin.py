import auth 
from datetime import timedelta 
from starlette import status 
from fastapi import HTTPException 


def register_admin(username: str, password: str, db):
    admin = auth.create_user(username, password, "admin")

    db.add(admin)
    db.commit()
    return {"Admin added."}

def is_valid_admin(username: str ,password: str, db):
    admin = auth.authenticate_admin(username, password, db)

    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could't validate admin")

    token = auth.create_access_token(admin.username, admin.id, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer'}


