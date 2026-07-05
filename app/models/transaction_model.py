from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Enum

from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    amount = Column(DECIMAL(10, 2), nullable=False)

    transaction_type = Column(
        Enum("income", "expense", name="transaction_type"),
        nullable=False
    )

    category = Column(String(50))
