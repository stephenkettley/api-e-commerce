from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Baskets, Products, Users
from src.repository.authentication import get_current_user, validate_correct_user
from src.repository.basket import is_basket_empty
from src.repository.payment import (
    does_user_have_enough_coupons,
    get_total_cost_of_product,
    has_user_paid_the_right_amount,
)
from src.routers.schemas.payment import PaymentBase
from src.routers.schemas.user import UserUnique

load_dotenv()

router = APIRouter(
    prefix="/payment",
    tags=["Payments"],
)


@router.post("/{id}", status_code=status.HTTP_200_OK, response_model=UserUnique)
def pay_for_unique_user_basket(
    id: int,
    payment: PaymentBase,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> UserUnique:
    """Pay for unique user's basket."""
    validate_correct_user(id=id, current_user_id=current_user.id)

    user_query = db.query(Users).filter(Users.id == id)
    user = user_query.first()

    basket_query = db.query(Baskets).filter(Baskets.user_id == id)
    basket_products = basket_query.all()

    is_basket_empty(basket_products=basket_products)
    does_user_have_enough_coupons(payment=payment, user=user)

    total_basket_cost = 0

    for basket_item in basket_products:
        product_query = db.query(Products).filter(Products.id == basket_item.product_id)
        product = product_query.first()
        total_basket_cost += get_total_cost_of_product(
            product=product, basket_item=basket_item
        )

    has_user_paid_the_right_amount(
        payment=payment,
        total_basket_cost=total_basket_cost,
    )
    new_coupons = payment.payment_amount // 5000

    user_query.update(
        {
            "total_spent_overall": user.total_spent_overall + payment.payment_amount,
            "coupon_count": user.coupon_count - payment.coupons_to_use + new_coupons,
        }
    )
    db.commit()

    user_query = db.query(Users).filter(Users.id == id)
    updated_user = user_query.first()

    basket_query.delete(synchronize_session=False)
    db.commit()

    return updated_user
