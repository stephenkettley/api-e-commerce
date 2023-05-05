from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Products, Users
from src.repository.authentication import get_current_user, validate_user_as_admin
from src.repository.product import does_product_exist_in_database
from src.routers.schemas.product import (
    ProductAll,
    ProductBase,
    ProductCreate,
    ShowProductStock,
    UpdateProductPrice,
    UpdateProductSalePercentage,
    UpdateProductStock,
)

router = APIRouter(
    prefix="/product",
    tags=["Products"],
)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[ProductAll])
def get_all_products(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> list[ProductAll]:
    """Get all products from database."""
    products = db.query(Products).all()
    return products


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ProductBase)
def get_unique_product(
    id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> ProductBase:
    """Get a unique product from database."""
    product_query = db.query(Products).filter(Products.id == id)
    product = product_query.first()
    does_product_exist_in_database(product=product)

    return product


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProductBase)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> ProductBase:
    """Create a new product in the database."""
    validate_user_as_admin(current_user_email=current_user.email)

    new_product = Products(name=product.name, price=product.price, stock=product.stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put(
    "/stock/{id}", status_code=status.HTTP_200_OK, response_model=ShowProductStock
)
def increase_unique_product_stock(
    id: int,
    stock: UpdateProductStock,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> ShowProductStock:
    """Increase the stock of a unique product."""
    validate_user_as_admin(current_user_email=current_user.email)

    product_query = db.query(Products).filter(Products.id == id)
    product = product_query.first()
    does_product_exist_in_database(product=product)
    updated_stock = product.stock + stock.stock_increase
    product_query.update({"stock": updated_stock})
    db.commit()
    updated_product = db.query(Products).filter(Products.id == id).first()
    return updated_product


@router.put("/price/{id}", status_code=status.HTTP_200_OK, response_model=ProductBase)
def update_unique_product_price(
    id: int,
    price: UpdateProductPrice,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> ProductBase:
    """Update price of a unique product."""
    validate_user_as_admin(current_user_email=current_user.email)

    product_query = db.query(Products).filter(Products.id == id)
    product = product_query.first()
    does_product_exist_in_database(product=product)

    product_query.update({"price": price.new_price})
    db.commit()
    updated_product = db.query(Products).filter(Products.id == id).first()
    return updated_product


@router.put("/sale/{id}", status_code=status.HTTP_200_OK, response_model=ProductBase)
def put_unique_product_on_sale(
    id: int,
    sale: UpdateProductSalePercentage,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> ProductBase:
    """Update the sale percentage of a unique product."""
    validate_user_as_admin(current_user_email=current_user.email)

    product_query = db.query(Products).filter(Products.id == id)
    product = product_query.first()
    does_product_exist_in_database(product=product)

    product_query.update({"sale_percentage": sale.sale_percentage})
    db.commit()
    updated_product = db.query(Products).filter(Products.id == id).first()
    return updated_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unique_product(
    id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> None:
    """Delete a unique product."""
    validate_user_as_admin(current_user_email=current_user.email)

    product_query = db.query(Products).filter(Products.id == id)
    product = product_query.first()
    does_product_exist_in_database(product=product)

    product_query.delete(synchronize_session=False)
    db.commit()
