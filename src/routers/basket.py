from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Baskets, Products, Users
from src.repository.product import does_product_exist_in_database
from src.repository.user import does_user_exist_in_database
from src.routers.schemas.basket import BasketsBase, DeleteBasketProduct

router = APIRouter(
    prefix="/basket",
    tags=["Baskets"],
)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[BasketsBase])
def get_all_basket_items_for_all_users(
    db: Session = Depends(get_db),
) -> list[BasketsBase]:
    """Get all basket items from database."""
    basket_items = db.query(Baskets).all()
    return basket_items


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BasketsBase)
def create_new_basket_item(
    basket_item: BasketsBase, db: Session = Depends(get_db)
) -> BasketsBase:
    """Create a new basket item."""
    user_query = db.query(Users).filter(Users.id == basket_item.user_id)
    user = user_query.first()
    does_user_exist_in_database(user=user)

    product_query = db.query(Products).filter(Products.id == basket_item.product_id)
    product = product_query.first()
    does_product_exist_in_database(product=product)

    new_basket_item = Baskets(
        user_id=basket_item.user_id,
        product_id=basket_item.product_id,
        quantity=basket_item.quantity,
    )
    db.add(new_basket_item)
    db.commit()
    db.refresh(new_basket_item)

    return new_basket_item


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_unique_user_basket_information(id: int, db: Session = Depends(get_db)) -> dict:
    """Get detailed basket info for a unique user."""
    total_basket_items = 0
    total_basket_cost = 0
    basket_info_dict = {
        "user_id": id,
        "items": [],
        "total_items_in_basket": 0,
        "total_cost_of_basket": 0,
    }

    user_query = db.query(Users).filter(Users.id == id)
    user = user_query.first()
    does_user_exist_in_database(user=user)

    basket_query = db.query(Baskets).filter(Baskets.user_id == id).all()

    for item in basket_query:
        product_query = (
            db.query(Products).filter(Products.id == item.product_id).first()
        )
        product_name = product_query.name
        product_quantity = item.quantity
        total_basket_cost += (
            product_query.price
            - product_query.price * (product_query.sale_percentage / 100)
        ) * product_quantity
        total_basket_items += product_quantity
        product_dict = {"product": product_name, "quantity": product_quantity}
        basket_info_dict["items"].append(product_dict)
        basket_info_dict["total_items_in_basket"] = total_basket_items
        basket_info_dict["total_cost_of_basket"] = total_basket_cost

    return basket_info_dict


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unique_user_basket_item(
    id: int, product_id: DeleteBasketProduct, db: Session = Depends(get_db)
) -> None:
    """Delete a unique product from unique user's basket."""
    basket_query = db.query(Baskets).filter(Baskets.user_id == id)
    basket_product_query = basket_query.filter(
        Baskets.product_id == product_id.product_id
    )

    if not basket_product_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} has no basket item with id {product_id.product_id}",
        )
    else:
        basket_product_query.delete(synchronize_session=False)
        db.commit()
