from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Users


def does_user_exist_in_database(user: Users) -> None:
    """Checks to see if a user exists in the 'users' table."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user does not exist",
        )
