# backend/app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

def get_products(db: Session):
    """List all products."""
    return db.query(models.Product).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_order(db: Session, order_in: schemas.OrderCreate):
    """Place a new order in 'pending' state."""
    # ensure product exists
    product = get_product(db, order_in.product_id)
    if not product:
        return None

    new_order = models.Order(
        product_id=order_in.product_id,
        quantity=order_in.quantity,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def get_order(db: Session, order_id: int):
    """Fetch order by ID."""
    return (
        db.query(models.Order)
          .filter(models.Order.id == order_id)
          .first()
    )
