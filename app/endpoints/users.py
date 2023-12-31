from fastapi import APIRouter, status, Depends, Response, Response
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import (
    UserRegisterSchema,
    UserResponseSchema,
    UserLoginSchema,
    TokenSchema,
    UserUpdateSchema,
)
from database import get_db, push_to_db
from typing import Dict
from utils import (
    create_access_token,
    create_refresh_token,
)
from sqlalchemy.future import select
from deps import get_current_user

authRouter = APIRouter(prefix="/api/users")


@authRouter.post("", response_model=Dict[str, UserResponseSchema])
async def register(
    payload: Dict[str, UserRegisterSchema], db: AsyncSession = Depends(get_db)
):
    user = User(**payload["user"].dict())
    result = await db.execute(select(User).where(User.email == user.email))
    user_exist = result.scalar_one_or_none()

    if user_exist:
        return Response(
            "User with this email already exist",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    else:
        await push_to_db(db, user)

    user.token = create_access_token(user.email)

    return {"user": user}


@authRouter.post("/login", response_model=Dict[str, UserResponseSchema])
async def login(
    payload: Dict[str, UserLoginSchema], db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == payload["user"].email))
    user = result.scalar_one_or_none()

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
async def login(
    payload: Dict[str, UserLoginSchema], db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == payload["user"].email))
    user = result.scalar_one_or_none()

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
async def update_user(
    payload: Dict[str, UserUpdateSchema],
    user: UserResponseSchema = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_update = payload["user"].dict(exclude_unset=True)

    for key, value in user_update.items():
        result = await db.execute(select(User).where(User.email == value))
        check_user_email = result.scalar_one_or_none()

        if key == "email" and check_user_email:
            return Response(
                "User with that email already exist",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        setattr(user, key, value)

    await push_to_db(db, user)

    return {"user": user}
