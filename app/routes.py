from fastapi import APIRouter
from typing import Optional


articleRouter = APIRouter(prefix="/articles")


@articleRouter.get("")
def list_articles(
    tag: Optional[str] = None,
    author: Optional[str] = None,
    favorited: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
):
    ...


@articleRouter.post("")
def create_article():
    ...


@articleRouter.get("/feed")
def feed_articles(
    limit: int = 20,
    offset: int = 0,
):
    ...


@articleRouter.get("/{slug}")
def get_article(
    slug: str,
    limit: int = 20,
    offset: int = 0,
):
    ...


@articleRouter.put("/{slug}")
def update_article(slug: str):
    ...


@articleRouter.delete("/{slug}")
def delete_article(slug: str):
    ...


@articleRouter.post("/{slug}/favorite")
def favorite_article(slug: str):
    ...


@articleRouter.delete("/{slug}/favorite")
def unfavorite_article(slug: str):
    ...


@articleRouter.post("/{slug}/comments")
def create_comment(slug: str):
    ...


@articleRouter.get("/{slug}/comments/{id}")
def get_comment(slug: str, id: int):
    ...


@articleRouter.delete("/{slug}/comments/{id}")
def delete_comment(slug: str, id: int):
    ...


tagRouter = APIRouter(prefix="/tag")


@tagRouter.get("")
def get_tags():
    ...


defaultRouter = APIRouter(prefix="/api")

defaultRouter.include_router(profileRouter)
defaultRouter.include_router(articleRouter)
defaultRouter.include_router(tagRouter)
