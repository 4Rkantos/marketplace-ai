from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.solution import crud
from models.solution import SolutionCreate, SolutionResponse  # Pydantic Models
from database.config import get_db

app = APIRouter()

@app.post("/solution/", response_model=SolutionResponse)
def create_solution(solution: SolutionCreate, db: Session = Depends(get_db)):
    return crud.create_solution(db=db, solution=solution)

@app.get("/solutions/{solution_id}", response_model=SolutionResponse)
def read_solution(solution_id: int, db: Session = Depends(get_db)):
    db_solution = crud.get_solution(db, solution_id=solution_id)
    if db_solution is None:
        raise HTTPException(status_code=404, detail="Solution not found")
    return db_solution

@app.get("/solutions/", response_model=List[SolutionResponse])
def read_solutions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    solutions = crud.get_solutions(db, skip=skip, limit=limit)
    return solutions

@app.get("/solutions/category/{category}", response_model=List[SolutionResponse])
def read_solutions_by_category(category: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    solutions = crud.get_solutions_by_category(db, category=category, skip=skip, limit=limit)
    if not solutions:
        raise HTTPException(status_code=404, detail="No solutions found for this category")
    return solutions