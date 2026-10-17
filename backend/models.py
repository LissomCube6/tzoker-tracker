from sqlalchemy import Column, Integer, String, Float
from backend.database import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)  # DD-MM-YYYY
    type = Column(String, index=True)  # "spent" or "won"
    amount = Column(Float)


class Repayment(Base):
    __tablename__ = "repayments"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)  # DD-MM-YYYY
    amount = Column(Float)
