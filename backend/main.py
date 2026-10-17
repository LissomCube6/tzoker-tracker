from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.database import Base, engine, SessionLocal
from backend import schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tzoker Tracker API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Entries endpoints


@app.post("/entries/", response_model=schemas.EntryRead)
def create_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    return crud.create_entry(db, entry)


@app.get("/entries/", response_model=List[schemas.EntryRead])
def list_entries(
    db: Session = Depends(get_db),
    start_date: str | None = None,
    end_date: str | None = None,
    type: str | None = None,
):
    return crud.get_entries(db, start_date, end_date, type)

# Repayments endpoints


@app.post("/repayments/", response_model=schemas.RepaymentRead)
def create_repayment(repayment: schemas.RepaymentCreate, db: Session = Depends(get_db)):
    return crud.create_repayment(db, repayment)


@app.get("/repayments/", response_model=List[schemas.RepaymentRead])
def list_repayments(db: Session = Depends(get_db), start_date: str | None = None, end_date: str | None = None):
    return crud.get_repayments(db, start_date, end_date)
