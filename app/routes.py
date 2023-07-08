from fastapi import APIRouter
from typing import Optional


tagRouter = APIRouter(prefix="/tag")


@tagRouter.get("")
def get_tags():
    ...


defaultRouter = APIRouter(prefix="/api")

defaultRouter.include_router(profileRouter)
defaultRouter.include_router(articleRouter)
defaultRouter.include_router(tagRouter)
