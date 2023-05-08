from pydantic import BaseModel

from src.routers.schemas.basket import BasketProduct


class UserBase(BaseModel):
    """Pydantic model for showing basic user information."""

    id: int
    name: str
    email: str
    total_spent_overall: float
    coupon_count: int

    class Config:
        """ORM config class."""

        orm_mode = True

        schema_extra = {
            "example": {
                "name": "Adam Jones",
                "email": "adamjones@gmail.com",
                "total_spent_overall": 2500,
                "coupon_count": 12,
            }
        }


class UserAll(UserBase):
    """Pydantic model for showing all users."""

    id: int

    class Config:
        """ORM config class."""

        orm_mode = True

        schema_extra = {
            "example": {
                "name": "Adam Jones",
                "email": "adamjones@gmail.com",
                "total_spent_overall": 2500,
                "coupon_count": 12,
                "id": 2,
            }
        }


class UserCreate(BaseModel):
    """Pydantic model for creating a new user."""

    name: str
    email: str
    password: str

    class Config:
        """ORM config class."""

        orm_mode = True

        schema_extra = {
            "example": {
                "name": "Stephen Kettley",
                "email": "stephenkettley@gmail.com",
                "password": "password123",
            }
        }


class UserUpdate(BaseModel):
    """Pydantic model for updating user information."""

    name: str
    email: str

    class Config:
        """ORM config class."""

        orm_mode = True

        schema_extra = {
            "example": {
                "name": "John Smith",
                "email": "johnsmith@gmail.com",
            }
        }


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

        schema_extra = {
            "example": {
                "name": "Miles Teller",
                "email": "milesteller@gmail.com",
                "total_spent_overall": 120000,
                "coupon_count": 35,
                "basket_items": [
                    {"product_id": 2},
                    {"product_id": 4},
                ],
            }
        }


class UserCurrent(BaseModel):
    """Pydantic model for current logged in user."""

    id: int
    email: str

    class Config:
        """ORM config class."""

        orm_mode = True

        schema_extra = {
            "example": {
                "id": "2",
                "email": "tristanbester@gmail.com",
            }
        }
