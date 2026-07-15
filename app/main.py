from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.db import crud
from app.db.database import SessionLocal
from app.schemas.transaction_schema import (
    TransactionCreate, TransactionResponse)
from app.schemas.user_schema import UserRegister, UserLogin, UserResponse
from app.core.security import (
    hash_password, verify_password, create_access_token, decode_access_token)


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# DB SESSION DEPENDENCY


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- Helper function ------------------


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = crud.get_user_by_username(db, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# ----------- ROOT -------------------


@app.get("/")
def root():
    return {"message": "Finance Manager API is running"}


# ----------- USERS -------------------
@app.post("/register", response_model=UserResponse)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    # add new user to the database
    user = crud.create_user(
        db=db,
        username=user_data.username,
        password_hash=hash_password(user_data.password)
    )
    return user


@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, form_data.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ------------ USER -------------------


@app.get("/me", response_model=UserResponse)
def read_me(current_user=Depends(get_current_user)):
    return current_user

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


@app.get("/transactions")
def get_my_transactions(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_transactions(db, current_user.user_id)

# ----------- BALANCE -------------------


@app.get("/balance")
def get_my_balance(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    balance = crud.get_balance(db, current_user.user_id)

    return {
        "user_id": current_user.user_id,
        "balance": balance
    }
