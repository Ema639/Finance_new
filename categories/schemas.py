from pydantic import BaseModel, Field
from typing import Literal, Optional


class CategoryBase(BaseModel):
    name: str
    type: Literal['доход', 'расход']
    description: Optional[str] = Field(None, max_length=255)


class CategoryCreate(CategoryBase):
    user_id: int


class CategoryOut(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True