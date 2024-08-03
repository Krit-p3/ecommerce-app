
from pydantic import BaseModel 


class ClientRequest(BaseModel):
    username: str
    password: str
