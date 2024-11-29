from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, EmailStr

# Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Relacionamento One-to-Many entre User e Order
    orders = relationship("Order", back_populates="user")

# Schema base
class UserBase(BaseModel):
    email: EmailStr  
    
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True