from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Products
from src.routers.schemas.product import (
    ProductBase,
    ShowProductStock,
    UpdateProductStock,
)

router = APIRouter(
    prefix="/product",
    tags=["Products"],
)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[ProductBase])
def get_all_products(db: Session = Depends(get_db)) -> list[ProductBase]:
    """Get all products from database."""
    products = db.query(Products).all()
    return products


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ProductBase)
def get_unique_product(id: int, db: Session = Depends(get_db)) -> ProductBase:
    """Get a unique product from database."""
    product_query = db.query(Products).filter(Products.id == id)
    product = product_query.first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the product with id {id} does not exist",
        )

    return product


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProductBase)
def create_new_product(
    product: ProductBase, db: Session = Depends(get_db)
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
    id: int, new_stock: UpdateProductStock, db: Session = Depends(get_db)
) -> ShowProductStock:
    """Increase the stock of a unique product."""
    product_query = db.query(Products).filter(Products.id == id)
    product = product_query.first()

    updated_stock = product.stock + new_stock.stock_increase

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the product with id {id} does not exist",
        )

    product_query.update({"stock": updated_stock})
    db.commit()
    updated_product = db.query(Products).filter(Products.id == id).first()

    return updated_product