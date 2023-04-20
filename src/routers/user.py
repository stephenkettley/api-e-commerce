from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_connection import get_db
from src.database.models import Users
from src.database.password_hashing import Bcrypt
from src.routers.schemas.user import UserAll, UserBase, UserCreate, UserUpdate

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[UserAll])
def get_all_users(db: Session = Depends(get_db)) -> list[UserAll]:
    """Get all users from database."""
    users = db.query(Users).all()
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserBase)
def get_unique_user(id: int, db: Session = Depends(get_db)) -> UserBase:
    """Get a unique user from database."""
    user_query = db.query(Users).filter(Users.id == id)
    user = user_query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the user with id {id} does not exist",
        )

    return user


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserBase)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)) -> UserBase:
    """Create a new product in the database."""
    bcrypt_hasher = Bcrypt()
    hashed_password = bcrypt_hasher.get_hashed_password(user.password)
    new_user = Users(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=UserBase)
def update_unique_user_information(
    id: int, user_update: UserUpdate, db: Session = Depends(get_db)
) -> UserBase:
    """Update basic user information."""
    user_query = db.query(Users).filter(Users.id == id)
    user = user_query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the user with id {id} does not exist",
        )

    user_query.update({"name": user_update.name, "email": user_update.email})
    db.commit()
    updated_user = db.query(Users).filter(Users.id == id).first()

    return updated_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unique_user(id: int, db: Session = Depends(get_db)) -> None:
    """Delete a unique user."""
    fetched_user = db.query(Users).filter(Users.id == id)
    if not fetched_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} does not exist for deletion",
        )
    else:
        fetched_user.delete(synchronize_session=False)
        db.commit()
