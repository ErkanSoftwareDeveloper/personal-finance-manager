from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    transaction_type: Literal["income", "expense"]
    category: str = Field(min_length=1, max_length=50)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "amount": 100.00,
                "transaction_type": "income",
                "category": "Salary"
            }
        }
    )


class TransactionResponse(BaseModel):
    transaction_id: int
    user_id: int
    amount: Decimal
    transaction_type: Literal["income", "expense"]
    category: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "transaction_id": 1,
                "user_id": 1,
                "amount": 100.00,
                "transaction_type": "income",
                "category": "Salary"
            }
        }
    )
