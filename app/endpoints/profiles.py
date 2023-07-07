from fastapi import APIRouter, status, Depends, Response, Response
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import (
    UserRegisterSchema,
    UserResponseSchema,
    UserLoginSchema,
    TokenSchema,
    UserUpdateSchema,
    ProfileRequestSchema,
    ProfileResponseSchema,
)
from database import get_db, push_to_db
from typing import Dict
from utils import (
    create_access_token,
    create_refresh_token,
)
from sqlalchemy.future import select
from deps import get_current_user


profileRouter = APIRouter(prefix="/api/profiles")


@profileRouter.get("/{username}", response_model=Dict[str, ProfileResponseSchema])
async def get_profile(
    username: str,
    db: AsyncSession = Depends(get_db),
    user: UserResponseSchema = Depends(get_current_user),
):
    result = await db.execute(select(User).where(User.username == username))
    profile = result.scalar_one_or_none()

    if user is None:
        return Response(
            "User is not authenticated", status_code=status.HTTP_401_UNAUTHORIZED
        )

    if profile is None:
        return Response(
            "No user with that username", status_code=status.HTTP_400_BAD_REQUEST
        )

    follows = profile.id in user.following_ids

    return {
        "profile": ProfileResponseSchema(
            username=profile.username,
            image=profile.image,
            bio=profile.bio,
            following=follows,
        )
    }


@profileRouter.post(
    "/{username}/follow", response_model=Dict[str, ProfileResponseSchema]
)
async def get_profile(
    username: str,
    db: AsyncSession = Depends(get_db),
    user: UserResponseSchema = Depends(get_current_user),
):
    result = await db.execute(select(User).where(User.username == username))
    profile = result.scalar_one_or_none()

    if user is None:
        return Response(
            "User is not authenticated", status_code=status.HTTP_401_UNAUTHORIZED
        )

    if profile is None:
        return Response(
            "No user with that username", status_code=status.HTTP_400_BAD_REQUEST
        )

    setattr(user, "following_ids", [*user.following_ids, profile.id])

    await push_to_db(db, user)

    follows = profile.id in user.following_ids

    return {
        "profile": ProfileResponseSchema(
            username=profile.username,
            image=profile.image,
            bio=profile.bio,
            following=follows,
        )
    }


@profileRouter.delete(
    "/{username}/follow", response_model=Dict[str, ProfileResponseSchema]
)
async def get_profile(
    username: str,
    db: AsyncSession = Depends(get_db),
    user: UserResponseSchema = Depends(get_current_user),
):
    result = await db.execute(select(User).where(User.username == username))
    profile = result.scalar_one_or_none()

    if user is None:
        return Response(
            "User is not authenticated", status_code=status.HTTP_401_UNAUTHORIZED
        )

    if profile is None:
        return Response(
            "No user with that username", status_code=status.HTTP_400_BAD_REQUEST
        )

    setattr(
        user, "following_ids", [ids for ids in user.following_ids if ids != profile.id]
    )

    await push_to_db(db, user)

    follows = profile.id in user.following_ids

    return {
        "profile": ProfileResponseSchema(
            username=profile.username,
            image=profile.image,
            bio=profile.bio,
            following=follows,
        )
    }
