import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from src.routers.schemas.authentication import TokenData

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_encoded_jwt_access_token(data: dict) -> dict:
    """Creates an encoded jwt access token."""
    data_to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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
            access_token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM")
        )
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(id=user_id)
    except PyJWTError:
        raise credentials_exception


def get_current_user(access_token: str = Depends(oauth2_scheme)) -> callable:
    """Verifies and gets the user currently logged in."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_jwt_access_token(
        access_token=access_token,
        credentials_exception=credentials_exception,
    )
