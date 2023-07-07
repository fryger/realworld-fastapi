# from sqlalchemy import create_engine
from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_scoped_session,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLITE_DATABASE_URL = "sqlite+aiosqlite:///./realworld-example.sqlite"

engine = create_async_engine(
    SQLITE_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

Base = declarative_base()


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


async def push_to_db(db: AsyncSession, obj):
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
