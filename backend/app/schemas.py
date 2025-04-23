# backend/app/schemas.py

from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class OrderStatusEnum(str, Enum):
    pending   = "pending"
    completed = "completed"
    canceled  = "canceled"

# ▶︎ Product schemas
class ProductBase(BaseModel):
    name: str
    price: int

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

# ▶︎ Order schemas
class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class Order(OrderCreate):
    id: int
    status: OrderStatusEnum
    created_at: datetime
    product: Product   # nested product info

    class Config:
        orm_mode = True
