from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Baskets, Products, Users
from src.repository.payment import (
    does_user_have_enough_coupons,
    get_total_cost_of_basket,
    get_total_cost_of_product,
    has_user_paid_the_right_amount,
)
from src.repository.user import does_user_exist_in_database
from src.routers.schemas.payment import PaymentBase
from src.routers.schemas.user import UserUnique

router = APIRouter(
    prefix="/payment",
    tags=["Payments"],
)


@router.post("/{id}", status_code=status.HTTP_200_OK, response_model=UserUnique)
def pay_for_unique_user_basket(
    id: int, payment: PaymentBase, db: Session = Depends(get_db)
) -> UserUnique:
    """Pay for unique user's basket."""
    total_basket_cost = 0

    user_query = db.query(Users).filter(Users.id == id)
    user = user_query.first()
    does_user_exist_in_database(user=user)

    basket_query = db.query(Baskets).filter(Baskets.user_id == id)
    basket_products = basket_query.all()

    if not basket_products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} has no basket items!",
        )

    does_user_have_enough_coupons(payment=payment, user=user)

    total_basket_cost = get_total_cost_of_basket(basket_products=basket_products)

    has_user_paid_the_right_amount(
        payment=payment,
        total_basket_cost=total_basket_cost,
    )
    new_coupons = payment.payment_amount // 5000

    user_query.update(
        {
            "total_spent_overall": user.total_spent_overall + payment.payment_amount,
            "coupon_count": user.coupon_count + new_coupons,
        }
    )
    db.commit()

    user_query = db.query(Users).filter(Users.id == id)
    updated_user = user_query.first()

    basket_query.delete(synchronize_session=False)
    db.commit()

    return updated_user
