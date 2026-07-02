from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db import crud
from app.db.database import SessionLocal

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
@app.post("/transactions")
def create_transaction(user_id: int, amount: float, category: str, db: Session = Depends(get_db)):
    transaction = crud.create_transaction(db, user_id, amount, category)
    return {
        "message": "Transaction added",
        "transaction_id": transaction.transaction_id
    }

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
