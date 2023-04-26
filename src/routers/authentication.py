from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Users
from src.database.password_hashing import verify_login_password
from src.routers.schemas.user import UserLogin

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def user_login(user_credentials: UserLogin, db: Session = Depends(get_db)) -> dict:
    """Validate a user login."""
    user_query = db.query(Users).filter(Users.email == user_credentials.email)
    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid credentials",
        )

    if not verify_login_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid credentials",
        )

    return {"token": "here is your token"}
