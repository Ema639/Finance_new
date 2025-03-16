from decimal import Decimal

from pydantic import BaseModel, condecimal
from typing import Optional, Literal
from datetime import datetime


class TransactionBase(BaseModel):
    amount: condecimal(max_digits=10, decimal_places=2)
    type: Literal['доход', 'расход']
    description: Optional[str] = None
    category_id: Optional[int] = None


class TransactionCreate(TransactionBase):
    user_id: int
    amount: float


class TransactionOut(TransactionBase):
    id: int
    user_id: int
    date: datetime
    amount: float

    class Config:
        from_attributes = True