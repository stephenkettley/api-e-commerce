from pydantic import BaseModel


class UserBase(BaseModel):
    """Pydantic model for showing basic user information."""

    name: str
    email: str
    total_spent_overall: float
    coupon_count: int
    number_of_items_in_current_basket: int
    total_cost_of_current_basket: float

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
