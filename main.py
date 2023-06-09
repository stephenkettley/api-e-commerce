from fastapi import FastAPI

from src.database.database_connection import Base, engine
from src.routers import authentication, basket, payment, product, user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product.router)
app.include_router(user.router)
app.include_router(basket.router)
app.include_router(payment.router)
app.include_router(authentication.router)
