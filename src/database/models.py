from database_connection import Base
from sqlalchemy import Column, Float, Integer, String


class Products(Base):
    """Model for postgres table called 'products'."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)


class Users(Base):
    """Model for postgres table called 'users'."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    total_spent = Column(Float, default=0)
