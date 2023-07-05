from datetime import datetime
from typing import List, Union
from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    email: str
    username: str
    password: str


class UserLoginSchema(BaseModel):
    email: str
    password: str



class UserResponseSchema(BaseModel):
    id: int
    email: str
    username: str
    # password: str
    token: str
    bio: Union[str, None]
    image: Union[str, None]

    class Config:
        orm_mode = True
