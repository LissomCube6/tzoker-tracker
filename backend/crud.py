from sqlalchemy.orm import Session
from backend import models, schemas


# Entries CRUD
def create_entry(db: Session, entry: schemas.EntryCreate):
    db_entry = models.Entry(
        date=entry.date,
        type=entry.type,
        amount=entry.amount
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_entries(db: Session, start_date=None, end_date=None, type=None):
    q = db.query(models.Entry)

    if start_date:
        q = q.filter(models.Entry.date >= start_date)
    if end_date:
        q = q.filter(models.Entry.date <= end_date)
    if type:
        q = q.filter(models.Entry.type == type)

    return q.order_by(models.Entry.date).all()

# Repayments CRUD


def create_repayment(db: Session, repayment: schemas.RepaymentCreate):
    db_repayment = models.Repayment(
        date=repayment.date,
        amount=repayment.amount
    )
    db.add(db_repayment)
    db.commit()
    db.refresh(db_repayment)
    return db_repayment


def get_repayments(db: Session, start_date: str | None = None, end_date: str | None = None):
    q = db.query(models.Repayment)

    if start_date:
        q = q.filter(models.Repayment.date >= start_date)
    if end_date:
        q = q.filter(models.Repayment.date <= end_date)

    return q.order_by(models.Repayment.date).all()
