from fastapi import HTTPException, status

from src.database.models import Products


def does_product_exist_in_database(product: Products) -> None:
    """Checks to see if a product exists in the 'products' table."""
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="product does not exist",
        )
