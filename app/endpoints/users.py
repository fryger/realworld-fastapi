from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import Optional
from sqlalchemy.orm import Session
from models import User
from schemas import UserRegisterSchema
from database import get_db
from typing import Dict
from sqlalchemy.exc import IntegrityError

authRouter = APIRouter(prefix="/api/users")


@authRouter.post("")
async def register(
    payload: Dict[str, UserRegisterSchema], db: Session = Depends(get_db)
):
    new_user = User(**payload["user"].dict())

    user_exist = db.query(User).filter(User.email == new_user.email).first()

    if user_exist:
        return Response("User already exists", status_code=status.HTTP_200_OK)

    else:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    return Response("User created", status_code=status.HTTP_201_CREATED)


@authRouter.post("/login")
def login():
    ...


userRouter = APIRouter(prefix="/api/user")


@userRouter.get("")
def get_user():
    ...


@userRouter.put("")
def update_user():
    ...
