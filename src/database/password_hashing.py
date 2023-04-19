from abc import ABC, abstractmethod

from passlib.context import CryptContext

pwd_cxt_bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_cxt_scrypt = CryptContext(schemes=["scrypt"], deprecated="auto")


class PasswordHasher(ABC):
    """Abstract class for hashing passwords."""

    @abstractmethod
    def get_hashed_password(self, password: str) -> str:
        """Generates hashed version for given password."""


class Bcrypt(PasswordHasher):
    """Bcrypt password hasher."""

    def get_hashed_password(self, password: str) -> str:
        """Generates hashed password using bcrypt."""
        hashed_password = pwd_cxt_bcrypt.hash(password)
        return hashed_password


class Scrypt(PasswordHasher):
    """Scrypt password hasher."""

    def get_hashed_password(self, password: str) -> str:
        """Generates hashed password using scrypt."""
        hashed_password = pwd_cxt_scrypt.hash(password)
        return hashed_password
