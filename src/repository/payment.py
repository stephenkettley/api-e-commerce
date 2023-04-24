from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Baskets, Products, Users
from src.routers.schemas.payment import PaymentBase


def does_user_have_enough_coupons(
    payment: PaymentBase, user: Users
) -> None | HTTPException:
    """Checks to see if user has as many coupons as they are trying to use."""
    if payment.coupons_to_use > user.coupon_count:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"You do not have {payment.coupons_to_use} coupons!",
        )


def get_total_cost_of_basket(basket_products: list) -> float:
    """Gets the total price of a basket of products with different quantities."""
    total_basket_cost = 0
    for product in basket_products:
        total_basket_cost += get_total_cost_of_product(product=product)

    return total_basket_cost


def get_total_cost_of_product(product: Baskets, db: Session = Depends(get_db)) -> float:
    """Gets the total cost of a quantity of a specific product in user basket."""
    product_query = db.query(Products).filter(Products.id == product.product_id)
    product = product_query.first()

    product_quantity = product.quantity

    total_cost_of_item = (
        product.price - product.price * (product.sale_percentage / 100)
    ) * product_quantity

    return total_cost_of_item


def has_user_paid_the_right_amount(
    payment: PaymentBase, total_basket_cost: float
) -> None:
    """Checks to see if the user has paid too little or too much for the basket of goods."""
    if payment.payment_amount > total_basket_cost:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You have paid too much!",
        )
    elif payment.payment_amount < total_basket_cost:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You have paid too little!",
        )
