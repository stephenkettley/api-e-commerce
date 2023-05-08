import os

import jwt
import pytest

from src.routers.schemas.authentication import Token


def test_correct_user_login(client: callable, test_user: callable) -> None:
    """Tests the logging in of a correct user."""
    response = client.post(
        "/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    assert response.status_code == 200
    login_result = dict(Token(**response.json()))

    payload = jwt.decode(
        login_result["access_token"],
        os.getenv("SECRET_KEY"),
        algorithms=[os.getenv("ALGORITHM")],
    )
    user_id = payload.get("user_id")

    assert user_id == test_user["id"]
    assert login_result["token_type"] == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password", 403),
        ("stephenkettley@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password", 422),
        ("stephenkettley@gmail.com", None, 422),
    ],
)
def test_multiple_incorrect_user_logins(
    test_user: callable,
    client: callable,
    email: str,
    password: str,
    status_code: int,
) -> None:
    """Tests the logging in of a user."""
    response = client.post(
        "/login",
        data={
            "username": email,
            "password": password,
        },
    )
    assert response.status_code == status_code
