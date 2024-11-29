from sqlalchemy import Column, Integer, String, Float
from database.config import Base
from pydantic import BaseModel

# Model
class Solution(Base):
    __tablename__ = "solutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category = Column(String)

# Schema base
class SolutionBase(BaseModel):
    name: str
    description: str
    price: float
    category: str

class SolutionCreate(SolutionBase):
    pass

class SolutionResponse(SolutionBase):
    id: int

    class Config:
        orm_mode = True
