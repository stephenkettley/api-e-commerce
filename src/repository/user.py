from fastapi import HTTPException, status

from src.database.models import Users


def does_user_already_exist(user: Users) -> None:
    """Checks to see if a user exists in the 'users' table."""
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="user with that email already exists, please use a different email",
        )
