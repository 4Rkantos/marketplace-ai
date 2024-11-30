from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.order import crud
from models.order import OrderCreate, OrderResponse
from database.config import get_db
from api.utils.utils import get_current_user
from models.user import User

router = APIRouter()

@router.post("/order/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user) ):
    try:
        return crud.create_order(db=db, order=order)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao criar o pedido: " + str(e))


@router.get("/order/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return db_order

@router.get("/orders/", response_model=List[OrderResponse])
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return crud.get_orders(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao buscar pedidos: " + str(e))



@router.get("/orders/by-user/{user_id}", response_model=List[OrderResponse])
def get_orders_by_user_id(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        db_orders = crud.get_orders_by_user_id(db, user_id=user_id, skip=skip, limit=limit)
        if not db_orders:
            raise HTTPException(status_code=404, detail="Nenhum pedido encontrado para este usuário.")
        return db_orders
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao buscar pedidos do usuário: " + str(e))

