import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Baskets, Products, Users
from src.repository.authentication import (
    get_current_user,
    validate_correct_user,
    validate_correct_user_or_admin,
    validate_user_as_admin,
)
from src.repository.product import does_product_exist_in_database, is_there_enough_stock
from src.repository.user import does_user_exist_in_database
from src.routers.schemas.basket import BasketCreate, BasketsBase, DeleteBasketProduct

load_dotenv()

router = APIRouter(
    prefix="/basket",
    tags=["Baskets"],
)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[BasketsBase])
def get_all_basket_items(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> list[BasketsBase]:
    """Get all basket items from database."""
    basket_items = db.query(Baskets).filter(Baskets.user_id == current_user.id).all()
    return basket_items


@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=BasketsBase)
def create_new_basket_item(
    id: int,
    new_item: BasketCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> BasketsBase:
    """Create a new basket item."""
    validate_correct_user(id=id, current_user_id=current_user.id)

    user_query = db.query(Users).filter(Users.id == id)
    user = user_query.first()

    product_query = db.query(Products).filter(Products.id == new_item.product_id)
    product = product_query.first()
    does_product_exist_in_database(product=product)

    is_there_enough_stock(
        quantity_purchased=new_item.quantity,
        amount_of_stock=product.stock,
    )

    basket_item_query = (
        db.query(Baskets)
        .filter(Baskets.user_id == id)
        .filter(Baskets.product_id == new_item.product_id)
    )
    basket_item = basket_item_query.first()

    if basket_item is None:
        new_basket_item = Baskets(
            user_id=id,
            product_id=new_item.product_id,
            quantity=new_item.quantity,
        )
        db.add(new_basket_item)
        product_query.update({"stock": product.stock - new_item.quantity})
        db.commit()
        db.refresh(new_basket_item)
        return new_basket_item

    else:
        basket_item_query.update({"quantity": basket_item.quantity + new_item.quantity})
        product_query.update({"stock": product.stock - new_item.quantity})
        db.commit()
        basket_item_query = (
            db.query(Baskets)
            .filter(Baskets.user_id == id)
            .filter(Baskets.product_id == new_item.product_id)
        )
        updated_basket_item = basket_item_query.first()
        return updated_basket_item


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_unique_user_basket_information(
    id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> dict:
    """Get detailed basket info for a unique user."""
    validate_correct_user_or_admin(id=id, current_user=current_user)

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
    id: int,
    product_id: DeleteBasketProduct,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> None:
    """Delete a unique product from unique user's basket."""
    validate_correct_user(id=id, current_user_id=current_user.id)

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
