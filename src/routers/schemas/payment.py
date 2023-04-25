from pydantic import BaseModel


class PaymentBase(BaseModel):
    """Pydantic model for payment details."""

    payment_amount: float
    coupons_to_use: int

    class Config:
        """ORM config class."""

        orm_mode = True

        schema_extra = {
            "example": {
                "payment_amount": "3500",
                "coupons_to_use": 3,
            }
        }
