from fastapi import APIRouter, status, Depends, Response, Response
from sqlalchemy.ext.asyncio import AsyncSession
from models import Article, User
from schemas import (
    ArticleResponseSchema,
    ArticleRequestSchema,
    UserResponseSchema,
    ProfileResponseSchema,
)
from database import get_db, push_to_db
from typing import Dict, List
from utils import (
    create_access_token,
    create_refresh_token,
)
from sqlalchemy.future import select
from deps import get_current_user
from typing import Optional, Union

articleRouter = APIRouter(prefix="/api/articles")


@articleRouter.get(
    "", response_model=Dict[str, Union[List[ArticleResponseSchema], int]]
)
async def list_articles(
    tag: Optional[str] = None,
    author: Optional[str] = None,
    favorited: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Article).order_by(Article.createdAt))
    articles = result.scalars().all()

    if articles is None:
        return Response("No articles", status_code=status.HTTP_200_OK)

    for article in articles:
        result = await db.execute(select(User).where(User.id == article.author))
        author = result.scalar_one_or_none()
        article.favorited = False
        article.author = ProfileResponseSchema(
            username=author.username,
            image=author.image,
            bio=author.bio,
            following=False,
        )

    return {"articles": articles, "articlesCount": len(articles)}


@articleRouter.post("", response_model=Dict[str, ArticleResponseSchema])
async def create_article(
    payload: Dict[str, ArticleRequestSchema],
    user: UserResponseSchema = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    article = Article(**payload["article"].dict(), author=user.id)
    await push_to_db(db, article)

    article.favorited = False
    article.author = ProfileResponseSchema(
        username=user.username, image=user.image, bio=user.bio, following=False
    )

    return {"articles": article}


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
