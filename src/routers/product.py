from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Products
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
def get_all_products(db: Session = Depends(get_db)) -> list[ProductAll]:
    """Get all products from database."""
    products = db.query(Products).all()
    return products


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ProductBase)
def get_unique_product(id: int, db: Session = Depends(get_db)) -> ProductBase:
    """Get a unique product from database."""
    product_query = db.query(Products).filter(Products.id == id)
    product = product_query.first()

    does_product_exist_in_database(product=product)

    return product


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProductBase)
def create_new_product(
    product: ProductCreate, db: Session = Depends(get_db)
) -> ProductBase:
    """Create a new product in the database."""
    new_product = Products(name=product.name, price=product.price, stock=product.stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put(
    "/stock/{id}", status_code=status.HTTP_200_OK, response_model=ShowProductStock
)
def increase_unique_product_stock(
    id: int, stock: UpdateProductStock, db: Session = Depends(get_db)
) -> ShowProductStock:
    """Increase the stock of a unique product."""
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
    id: int, price: UpdateProductPrice, db: Session = Depends(get_db)
) -> ProductBase:
    """Update price of a unique product."""
    product_query = db.query(Products).filter(Products.id == id)
    product = product_query.first()

    does_product_exist_in_database(product=product)

    product_query.update({"price": price.new_price})
    db.commit()
    updated_product = db.query(Products).filter(Products.id == id).first()

    return updated_product


@router.put("/sale/{id}", status_code=status.HTTP_200_OK, response_model=ProductBase)
def put_unique_product_on_sale(
    id: int, sale: UpdateProductSalePercentage, db: Session = Depends(get_db)
) -> ProductBase:
    """Update the sale percentage of a unique product."""
    product_query = db.query(Products).filter(Products.id == id)
    product = product_query.first()

    does_product_exist_in_database(product=product)

    product_query.update({"sale_percentage": sale.sale_percentage})
    db.commit()
    updated_product = db.query(Products).filter(Products.id == id).first()

    return updated_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unique_product(id: int, db: Session = Depends(get_db)) -> None:
    """Delete a unique product."""
    product_query = db.query(Products).filter(Products.id == id)
    product = product_query.first()

    does_product_exist_in_database(product=product)

    product_query.delete(synchronize_session=False)
    db.commit()
