from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Users
from src.database.password_hashing import Bcrypt
from src.repository.authentication import (
    get_current_user,
    validate_correct_user,
    validate_correct_user_or_admin,
    validate_user_as_admin,
)
from src.repository.user import does_user_already_exist
from src.routers.schemas.user import (
    UserAll,
    UserBase,
    UserCreate,
    UserUnique,
    UserUpdate,
)

load_dotenv()

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[UserBase])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> list[UserBase]:
    """Get all users from database."""
    validate_user_as_admin(current_user_email=current_user.email)
    users = db.query(Users).all()

    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserUnique)
def get_unique_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> UserUnique:
    """Get a unique user from database."""
    validate_correct_user_or_admin(id=id, current_user=current_user)
    user_query = db.query(Users).filter(Users.id == id)
    user = user_query.first()
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserBase)
def create_new_user(
    new_user: UserCreate,
    db: Session = Depends(get_db),
) -> UserBase:
    """Create a new product in the database."""
    user_query = db.query(Users).filter(Users.email == new_user.email)
    user = user_query.first()
    does_user_already_exist(user=user)

    bcrypt_hasher = Bcrypt()
    hashed_password = bcrypt_hasher.get_hashed_password(new_user.password)
    new_user_to_add = Users(
        name=new_user.name, email=new_user.email, hashed_password=hashed_password
    )
    db.add(new_user_to_add)
    db.commit()
    db.refresh(new_user_to_add)
    return new_user_to_add


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=UserBase)
def update_unique_user_information(
    id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> UserBase:
    """Update basic user information."""
    validate_correct_user(id=id, current_user_id=current_user.id)

    user_query = db.query(Users).filter(Users.id == id)
    user_query.update({"name": user_update.name, "email": user_update.email})
    db.commit()

    updated_user = db.query(Users).filter(Users.id == id).first()
    return updated_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unique_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> None:
    """Delete a unique user."""
    validate_correct_user(id=id, current_user_id=current_user.id)

    user_query = db.query(Users).filter(Users.id == id)
    user = user_query.first()
    user.delete(synchronize_session=False)
    db.commit()
