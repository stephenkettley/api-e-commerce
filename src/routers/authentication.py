from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Users
from src.database.password_hashing import verify_login_password
from src.repository.authentication import create_encoded_jwt_access_token
from src.routers.schemas.authentication import Token

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def user_login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """Validate a user login."""
    user_query = db.query(Users).filter(Users.email == user_credentials.username)
    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid credentials",
        )

    if not verify_login_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid credentials",
        )

    encoded_jwt_access_token = create_encoded_jwt_access_token(
        data={"user_id": user.id}
    )

    return {
        "access_token": encoded_jwt_access_token,
        "token_type": "bearer",
    }
