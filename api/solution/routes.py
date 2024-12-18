from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.solution import crud
from models.solution import SolutionCreate, SolutionResponse  # Pydantic Models
from database.config import get_db
from models.user import User
from api.utils.utils import is_admin, get_current_user

router = APIRouter()

@router.post("/solution/", response_model=SolutionResponse)
def create_solution(solution: SolutionCreate, db: Session = Depends(get_db), admin: User = Depends(is_admin)):
    return crud.create_solution(db=db, solution=solution)

@router.get("/solutions/{solution_id}", response_model=SolutionResponse)
def read_solution(solution_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_solution = crud.get_solution(db, solution_id=solution_id)
    if db_solution is None:
        raise HTTPException(status_code=404, detail="Solução não encontrada")
    return db_solution

@router.get("/solutions/", response_model=List[SolutionResponse])
def read_solutions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    solutions = crud.get_solutions(db, skip=skip, limit=limit)
    return solutions

@router.get("/solutions/category/{category}", response_model=List[SolutionResponse])
def read_solutions_by_category(category: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    solutions = crud.get_solutions_by_category(db, category=category, skip=skip, limit=limit)
    if not solutions:
        raise HTTPException(status_code=404, detail="Nenhuma solução encontrada para esta categoria")
    return solutions