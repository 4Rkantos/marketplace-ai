from sqlalchemy import Column, Integer, String
from database.config import Base
from pydantic import BaseModel, EmailStr

# Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

# Schema base
class UserBase(BaseModel):
    email: EmailStr  
    
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True