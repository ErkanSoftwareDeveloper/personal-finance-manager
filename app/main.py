from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, crud
from app.database import SessionLocal, engine

app = FastAPI()


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
