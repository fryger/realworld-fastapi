from datetime import datetime
from typing import List, Union
from pydantic import BaseModel
from datetime import datetime


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserRegisterSchema(BaseModel):
    email: str
    username: str
    password: str


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    email: Union[str, None]
    username: Union[str, None]
    password: Union[str, None]
    image: Union[str, None]
    bio: Union[str, None]


class UserResponseSchema(BaseModel):
    id: int
    email: str
    username: str
    token: Union[str, None]
    bio: Union[str, None]
    image: Union[str, None]
    following_ids: Union[list, None]

    class Config:
        orm_mode = True


class ProfileRequestSchema(BaseModel):
    email: str


class ProfileResponseSchema(BaseModel):
    username: Union[str, None]
    image: Union[str, None]
    bio: Union[str, None]
    following: Union[bool, None]


class ArticleResponseSchema(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tagList: Union[list, None]
    createdAt: datetime
    updatedAt: datetime
    favorited: bool
    favoritesCount: int
    author: ProfileResponseSchema

    class Config:
        orm_mode = True


class ArticleRequestSchema(BaseModel):
    title: str
    description: str
    body: str
    tagList: Union[List[str], None]
