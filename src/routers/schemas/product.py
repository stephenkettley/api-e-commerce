from pydantic import BaseModel


class ProductBase(BaseModel):
    """Pydantic model for showing basic product information."""

    name: str
    price: float
    stock: int
    sale_percentage: int

    class Config:
        """ORM config class."""

        orm_mode = True


class ProductCreate(BaseModel):
    """Pydantic model for creating a new product."""

    name: str
    price: float
    stock: int

    class Config:
        """ORM config class."""

        orm_mode = True


class ProductAll(ProductBase):
    """Pydantic model for showing all products."""

    id: int

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


class UpdateProductPrice(BaseModel):
    """Pydantic model for updating price of products."""

    new_price: float

    class Config:
        """ORM config class."""

        orm_mode = True


class UpdateProductSalePercentage(BaseModel):
    """Pydantic model for updating sale percentage of products."""

    sale_percentage: int

    class Config:
        """ORM config class."""

        orm_mode = True
