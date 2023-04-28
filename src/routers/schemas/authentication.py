from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Pydantic model for a jwt access token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Pydantic model for data within payload of a jwt access token."""

    id: Optional[str] = None
