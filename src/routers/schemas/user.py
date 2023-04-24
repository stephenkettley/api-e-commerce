from pydantic import BaseModel

from src.routers.schemas.basket import BasketProduct


class UserBase(BaseModel):
    """Pydantic model for showing basic user information."""

    name: str
    email: str
    total_spent_overall: float
    coupon_count: int

    class Config:
        """ORM config class."""

        orm_mode = True


class UserAll(UserBase):
    """Pydantic model for showing all users."""

    id: int

    class Config:
        """ORM config class."""

        orm_mode = True


class UserCreate(BaseModel):
    """Pydantic model for creating a new user."""

    name: str
    email: str
    password: str

    class Config:
        """ORM config class."""

        orm_mode = True


class UserUpdate(BaseModel):
    """Pydantic model for updating user information."""

    name: str
    email: str

    class Config:
        """ORM config class."""

        orm_mode = True


class UserUnique(BaseModel):
    """Pydantic model for showing a unique user."""

    name: str
    email: str
    total_spent_overall: float
    coupon_count: int
    basket_items: list[BasketProduct]

    class Config:
        """ORM config class."""

        orm_mode = True
