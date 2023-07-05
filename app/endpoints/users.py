from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.orm import Session
from models import User
from schemas import (
    UserRegisterSchema,
    UserResponseSchema,
    UserLoginSchema,
    TokenSchema,
    UserUpdateSchema,
)
from database import get_db
from typing import Dict
from sqlalchemy.exc import IntegrityError
from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
)

from deps import get_current_user

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


@authRouter.post("/jwtlogin", response_model=TokenSchema)
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

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


userRouter = APIRouter(prefix="/api/user")


@userRouter.get("", response_model=Dict[str, UserResponseSchema])
async def get_user(user: UserResponseSchema = Depends(get_current_user)):
    return {"user": user}


@userRouter.put("", response_model=Dict[str, UserResponseSchema])
def update_user(
    payload: Dict[str, UserUpdateSchema],
    user: UserResponseSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_update = payload["user"].dict(exclude_unset=True)

    for key, value in user_update.items():
        if key == "email" and (
            check_user_email := db.query(User).filter(User.email == value).first()
        ):
            return Response(
                "User with that email already exist",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"user": user}
