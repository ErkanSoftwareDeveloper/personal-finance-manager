from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    user_id: int
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)

    transaction_type: Literal["income", "expense"]

    category: str = Field(min_length=1, max_length=50)


class TransactionResponse(BaseModel):
    transaction_id: int
    user_id: int
    amount: Decimal
    transaction_type: Literal["income", "expense"]
    category: str | None = None

    class Config:
        from_attributes = True
