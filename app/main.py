from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import crud
from app.db.database import SessionLocal
from app.schemas.transaction_schema import (
    TransactionCreate, TransactionResponse)


app = FastAPI()


# DB SESSION DEPENDENCY

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------- ROOT -------------------


@app.get("/")
def root():
    return {"message": "Finance Manager API is running"}


# ----------- USERS -------------------
@app.post("/register")
def register_user(username: str, password: str, db: Session = Depends(get_db)):
    # add new user to the database
    user = crud.create_user(db, username, password)

    return {
        "message": "User created",
        "user_id": user.user_id
    }


# ------------ USER get BY ID-------------------
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    return user


# ----------- TRANSACTIONS -------------------
@app.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED
)
def add_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db)
):

    user = crud.get_user(db, transaction_data.user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return crud.create_transaction(
        db=db,
        user_id=transaction_data.user_id,
        amount=transaction_data.amount,
        transaction_type=transaction_data.transaction_type,
        category=transaction_data.category
    )

# ----------- TRANSACTIONS List -------------------


@app.get("/transactions/{user_id}")
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    return crud.get_transactions(db, user_id)

# ----------- BALANCE -------------------


@app.get("/balance/{user_id}")
def get_balance(user_id: int, db: Session = Depends(get_db)):
    balance = crud.get_balance(db, user_id)

    return {
        "user_id": user_id,
        "balance": balance
    }
