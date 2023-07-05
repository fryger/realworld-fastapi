from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.orm import Session
from models import User
from schemas import UserRegisterSchema, UserResponseSchema, UserLoginSchema
from database import get_db
from typing import Dict
from sqlalchemy.exc import IntegrityError
from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
)

authRouter = APIRouter(prefix="/api/users")


@authRouter.post("", response_model=Dict[str, UserResponseSchema])
async def register(
    payload: Dict[str, UserRegisterSchema], db: Session = Depends(get_db)
):
    user = User(**payload["user"].dict())

    user_exist = db.query(User).filter(User.email == user.email).first()

    if user_exist:
        return Response(
            "User with this email already exist",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    else:
        db.add(user)
        db.commit()
        db.refresh(user)

    user.token = create_access_token(user.email)

    return {"user": user}


@authRouter.post("/login", response_model=Dict[str, UserResponseSchema])
async def login(payload: Dict[str, UserLoginSchema], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload["user"].email).first()

    if user is None:
        return Response(
            "User does not exist",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if user.password != payload["user"].password:
        return Response(
            "Incorrect password",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user.token = create_access_token(user.email)

    return {"user": user}


userRouter = APIRouter(prefix="/api/user")


@userRouter.get("")
def get_user():
    ...


@userRouter.put("")
def update_user():
    ...
