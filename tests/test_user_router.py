from fastapi.testclient import TestClient

from main import app
from src.routers.schemas.user import UserBase

client = TestClient(app)


def test_create_new_user() -> None:
    """Tests user gets created correctly."""
    response = client.post(
        "/user/",
        json={
            "name": "test",
            "email": "test@gmail.com",
            "password": "test",
        },
    )
    new_user = UserBase(**response.json())
    assert new_user.name == "test"
    assert new_user.email == "test@gmail.com"
    assert response.status_code == 201


def test_create_user_that_already_exists() -> None:
    """Tests that correct HTTPException raised when creating an exisiting user."""
    response = client.post(
        "/user/",
        json={
            "name": "tristan bester",
            "email": "tristanbester@gmail.com",
            "password": "coding",
        },
    )
    assert response.status_code == 406
