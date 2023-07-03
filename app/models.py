from database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy_utils import EmailType, PasswordType, URLType


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
