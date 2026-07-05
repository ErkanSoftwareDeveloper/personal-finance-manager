from sqlalchemy.orm import Session
from app import models
from decimal import Decimal

# ------------ CREATE USER-------------------


def create_user(db: Session, username: str, password_hash: str):
    user = models.User(
        username=username,
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

# get user by id


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(
        models.User.user_id == user_id
    ).first()

# get user by username


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username
    ).first()


# ------------ TRANSACTION FUNCTIONS -------------------
def create_transaction(db: Session, user_id: int, amount: Decimal, category: str, transaction_type: str):
    transaction = models.Transaction(
        user_id=user_id,
        amount=amount,
        category=category,
        transaction_type=transaction_type
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


# ------------ BALANCE LOGIC -------------------

def get_balance(db: Session, user_id: int):
    transactions = get_transactions(db, user_id)

    balance = Decimal("0.00")

    for transaction in transactions:
        if transaction.transaction_type == "income":
            balance += transaction.amount

        elif transaction.transaction_type == "expense":
            balance -= transaction.amount

    return balance

# --------- Get_transactions -------------------


def get_transactions(db: Session, user_id: int):
    return db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id
    ).all()
