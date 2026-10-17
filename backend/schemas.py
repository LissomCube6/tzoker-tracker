from pydantic import BaseModel

class EntryBase(BaseModel):
    date: str  # DD-MM-YYYY
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
    date: str  # DD-MM-YYYY
    amount: float

class RepaymentCreate(RepaymentBase):
    pass

class RepaymentRead(RepaymentBase):
    id: int

    class Config:
        from_attributes = True

