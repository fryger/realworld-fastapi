from datetime import datetime
from typing import List, Union
from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    # id: int
    email: str
    username: str
    password: str
    # bio: str
    # image: str

    # class Config:
    #     orm_mode = True
