from fastapi import HTTPException, status

from src.database.models import Baskets


def does_product_exist_in_user_basket(basket_product: Baskets) -> None:
    """Checks to see whether a product exists in a user basket."""
    if not basket_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="that product does not exist in the basket",
        )


def is_basket_empty(basket_products: list) -> None:
    """Checks if a user's basket is empty."""
    if not basket_products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user has no basket items!",
        )
