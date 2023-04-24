from pydantic import BaseModel


class PaymentBase(BaseModel):
    """Pydantic model for payment details."""

    payment_amount: float
    coupons_to_use: int

    class Config:
        """ORM config class."""

        orm_mode = True
