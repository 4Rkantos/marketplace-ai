from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel
from typing import List

# Tabela associativa para relacionar Orders e Solutions
order_solutions = Table(
    "order_solutions",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("solution_id", Integer, ForeignKey("solutions.id"), primary_key=True),
)

# Model
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Relacionamento com User
    status = Column(String, index=True)

    # Relacionamento Many-to-One entre Order e User
    user = relationship("User", back_populates="orders")

    # Relacionamento Many-to-Many com Solution
    solutions = relationship("Solution", secondary=order_solutions, back_populates="orders")

# Schema base
class OrderBase(BaseModel):
    user_id: int
    status: str

class OrderCreate(OrderBase):
    solution_ids: List[int]  # Lista de IDs de soluções no pedido

class OrderResponse(OrderBase):
    id: int
    solution_ids: List[int]  # Lista de IDs de soluções no pedido

    class Config:
        orm_mode = True