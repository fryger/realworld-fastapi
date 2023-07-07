from database import Base
from sqlalchemy import Column, String, Integer, ARRAY
from sqlalchemy_utils import EmailType, PasswordType, URLType

from sqlalchemy.types import TypeDecorator, TEXT, VARCHAR


class TextArray(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = ", ".join(str(num) for num in value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = [int(num) for num in value.split(", ")]

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
