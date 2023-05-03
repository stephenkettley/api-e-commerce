import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Users
from src.routers.schemas.authentication import TokenData

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_encoded_jwt_access_token(data: dict) -> dict:
    """Creates an encoded jwt access token."""
    data_to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})

    encoded_jwt_token = jwt.encode(
        data_to_encode,
        os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM"),
    )

    return encoded_jwt_token


def verify_jwt_access_token(
    access_token: str, credentials_exception: Exception
) -> None:
    """Verifies the validity of a jwt access token."""
    try:
        payload = jwt.decode(
            access_token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(id=user_id)
    except PyJWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Users:
    """Verifies and gets the user currently logged in."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_jwt_access_token(
        access_token=access_token,
        credentials_exception=credentials_exception,
    )
    user = db.query(Users).filter(Users.id == token.id).first()
    return user


def validate_correct_user(id: int, current_user_id: int) -> None:
    """Validates whether a user is authorized correctly."""
    if id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform this requested action",
        )


def validate_user_as_admin(current_user_email: str) -> None:
    """Validates whether a user is authorized correctly."""
    if current_user_email != os.getenv("USER_ADMIN_EMAIL"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform this requested action",
        )


def validate_correct_user_or_admin(id: int, current_user: Users) -> None:
    """Validates whether a user is authorized correctly."""
    if (id != current_user.id) & (current_user.email != os.getenv("USER_ADMIN_EMAIL")):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform this requested action",
        )
