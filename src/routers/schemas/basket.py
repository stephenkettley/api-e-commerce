from pydantic import BaseModel


class BasketsBase(BaseModel):
    """Pydantic model for showing general basket items information."""

    user_id: int
    product_id: int
    quantity: int

    class Config:
        """ORM config class."""

        orm_mode = True


class DeleteBasketProduct(BaseModel):
    """Pydantic model for deleting product from a user basket."""

    product_id: int

    class Config:
        """ORM config class."""

        orm_mode = True


class BasketProduct(BaseModel):
    """Pydantic model for displaying product in user's basket."""

    product_id: int

    class Config:
        """ORM config class."""

        orm_mode = True
