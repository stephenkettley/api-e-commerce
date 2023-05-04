from src.routers.schemas.user import UserBase
from tests.database import client, session


def test_create_new_user(client: callable) -> None:
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
    assert new_user.total_spent_overall == 0
    assert new_user.coupon_count == 0
    assert response.status_code == 201
