from pydantic import BaseModel


class BasketsBase(BaseModel):
    """Pydantic model for showing basket item information."""

    user_id: int
    product_id: int
    quantity: int

    class Config:
        """ORM config class."""

        orm_mode = True
