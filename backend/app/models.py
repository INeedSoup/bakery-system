# backend/app/models.py

import enum
import datetime
from sqlalchemy import (
    Column, Integer, String,
    Enum, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from .database import Base

class OrderStatusEnum(str, enum.Enum):
    pending   = "pending"
    completed = "completed"
    canceled  = "canceled"

class Product(Base):
    __tablename__ = "products"

    id    = Column(Integer, primary_key=True, index=True)
    name  = Column(String, unique=True, nullable=False)
    price = Column(Integer, nullable=False)

    # optional: back-reference to orders
    orders = relationship("Order", back_populates="product")

class Order(Base):
    __tablename__ = "orders"

    id         = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity   = Column(Integer, nullable=False)
    status     = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    product = relationship("Product", back_populates="orders")
