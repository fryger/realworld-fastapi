from database import Base
from sqlalchemy import Column, String, Integer, event, DateTime, ForeignKey
from sqlalchemy_utils import EmailType, PasswordType, URLType
from sqlalchemy.types import TypeDecorator, TEXT
from sqlalchemy.sql import func
from slugify import slugify
from sqlalchemy.orm import relationship


class TextArray(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = ", ".join(str(num) for num in value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = [int(num) if num.isnumeric() else num for num in value.split(", ")]

        else:
            value = []
        return value


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(EmailType, nullable=False)
    password = Column(
        PasswordType(
            schemes=["pbkdf2_sha512"],
        ),
        nullable=False,
        unique=True,
    )
    username = Column(String(30), nullable=False, unique=True)
    bio = Column(String(500))
    image = Column(URLType)
    following_ids = Column(TextArray)
    articles = relationship("Article", backref="users")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    slug = Column(String(255))
    description = Column(String(255))
    body = Column(String(999999999))
    tagList = Column(TextArray)
    createdAt = Column(
        DateTime(timezone=True), server_default=func.now(), default=func.now()
    )
    updatedAt = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        default=func.now(),
    )
    favoritesCount = Column(Integer, default=0)
    author = Column(Integer, ForeignKey("users.id"))

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        print(target)
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)


event.listen(Article.title, "set", Article.generate_slug, retval=False)
