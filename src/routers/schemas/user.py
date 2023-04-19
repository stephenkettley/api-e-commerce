from pydantic import BaseModel


class UserBase(BaseModel):
    """Pydantic model for showing basic user information."""

    name: str
    email: str
    total_spent: float
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
