from pydantic import BaseModel

class EntryBase(BaseModel):
    date: str  # ISO 8601 date (YYYY-MM-DD)
    type: str  # "spent" or "won"
    amount: float

class EntryCreate(EntryBase):
    pass

class EntryRead(EntryBase):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True

# Repayment schemas
class RepaymentBase(BaseModel):
    date: str  # ISO 8601 date (YYYY-MM-DD)
    amount: float

class RepaymentCreate(RepaymentBase):
    pass

class RepaymentRead(RepaymentBase):
    id: int

    class Config:
        from_attributes = True
