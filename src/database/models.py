from sqlalchemy import Column, Float, Integer, String

from src.database.database_connection import Base


class Products(Base):
    """Model for postgres table called 'products'."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, server_default="0")
    sale_percentage = Column(Integer, server_default="0")


class Users(Base):
    """Model for postgres table called 'users'."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    total_spent_overall = Column(Float, server_default="0")
    coupon_count = Column(Integer, server_default="0")
    number_of_items_in_current_basket = Column(Integer, server_default="0")
    total_cost_of_current_basket = Column(Float, server_default="0")
