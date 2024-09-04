from datetime import datetime

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    is_active: bool


class ProductRead(BaseModel):
    id: int
    name: str
    price: float
    created_at: datetime
    updated_at: datetime
    is_active: bool


class ProductUpdate(BaseModel):
    name: str
    price: float
    is_active: bool
