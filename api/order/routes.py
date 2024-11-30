from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.order import crud
from models.order import OrderCreate, OrderResponse
from database.config import get_db

app = APIRouter()

@app.post("/order/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)


@app.get("/order/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.get("/orders/", response_model=List[OrderResponse])
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_orders = crud.get_orders(db, skip=skip, limit=limit)
    return db_orders


@app.get("/orders/by-user/{user_id}", response_model=List[OrderResponse])
def get_orders_by_user_id(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_orders = crud.get_orders_by_user_id(db, user_id=user_id, skip=skip, limit=limit)
    return db_orders

