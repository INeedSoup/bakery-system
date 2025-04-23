from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal, Base
from .messaging import publish_order_message
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bakery API",
    description="API for managing bakery products and orders with RabbitMQ integration",
    version="1.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---

@app.get("/products", 
         response_model=list[schemas.Product],
         summary="List all products",
         tags=["Products"])
def list_products(db: Session = Depends(get_db)):
    """Retrieve a list of all available bakery products"""
    return crud.get_products(db)

@app.post("/orders", 
          response_model=schemas.Order,
          status_code=status.HTTP_201_CREATED,
          summary="Create a new order",
          tags=["Orders"])
def place_order(order_in: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new bakery order and publish it to RabbitMQ
    
    - **order_in**: Order details including products and quantities
    - Returns: The created order with status information
    """
    order = crud.create_order(db, order_in)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more products not found"
        )
    
    # Publish order to RabbitMQ
    try:
        publish_order_message(order)
        logger.info(f"Successfully published order {order.id} to RabbitMQ")
    except Exception as e:
        logger.error(f"Failed to publish order {order.id} to RabbitMQ: {str(e)}", 
                   exc_info=True)
        # Continue despite RabbitMQ failure to maintain order processing
    
    return order

@app.get("/orders/{order_id}", 
         response_model=schemas.Order,
         summary="Get order details",
         tags=["Orders"])
def check_order(order_id: int, db: Session = Depends(get_db)):
    """Retrieve details of a specific order by ID"""
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

@app.get("/health", 
         tags=["Health"],
         summary="Check API health")
def health():
    """Check if the API is running and connected to dependencies"""
    return {
        "status": "ok",
        "details": {
            "database": "connected",
            "rabbitmq": "unknown"  # You could add actual status checks
        }
    }