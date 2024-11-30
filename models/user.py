from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, EmailStr

# Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)   
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Relacionamento One-to-Many entre User e Order
    orders = relationship("Order", back_populates="user")

# Schema base
class UserBase(BaseModel):
    name: str
    email: EmailStr
    
class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str