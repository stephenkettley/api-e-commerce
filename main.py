from fastapi import FastAPI

from src.database.database_connection import Base, engine
from src.routers import product

Base.metadata.create_all(bind=engine)  # creates the tables in postgres

app = FastAPI()

app.include_router(product.router)
