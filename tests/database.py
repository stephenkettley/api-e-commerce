import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.database.database_connection import Base, get_db

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:bornfreebeing@localhost/ecommerce_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session() -> None:
    """Database logic."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session: callable) -> TestClient:
    """Returns TestClient object."""

    def override_get_db() -> None:
        """Creates a new session to the database."""
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# the above fixtures allows us to get access to the database in our tests if we wanted to query it
