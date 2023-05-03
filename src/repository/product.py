from fastapi import HTTPException, status

from src.database.models import Products


def does_product_exist_in_database(product: Products) -> None:
    """Checks to see if a product exists in the 'products' table."""
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="product does not exist",
        )


def is_there_enough_stock(
    quantity_purchased: int,
    amount_of_stock: int,
) -> None:
    """Checks if there is enough stock left for a specific item."""
    if quantity_purchased > amount_of_stock:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"there are only {amount_of_stock} items left for this product",
        )
