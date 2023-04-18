from pydantic import BaseModel


class ProductBase(BaseModel):
    """Pydantic model for showing all products."""

    name: str
    price: float
    stock: int

    class Config:
        """ORM config class."""

        orm_mode = True


class ShowProductStock(BaseModel):
    """Pydantic model for showing product after stock increase."""

    name: str
    stock: int

    class Config:
        """ORM config class."""

        orm_mode = True


class UpdateProductStock(BaseModel):
    """Pydantic model for updating stock of products."""

    stock_increase: int

    class Config:
        """ORM config class."""

        orm_mode = True
