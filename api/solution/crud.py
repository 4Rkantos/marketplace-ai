from sqlalchemy.orm import Session
from models.solution import Solution  # SQLAlchemy Model
from models.solution import SolutionCreate  # Pydantic Model for creation

def get_solution(db: Session, solution_id: int):
    # Query using the SQLAlchemy model
    return db.query(Solution).filter(Solution.id == solution_id).first()

def get_solutions(db: Session, skip: int = 0, limit: int = 10):
    # Query using the SQLAlchemy model
    return db.query(Solution).offset(skip).limit(limit).all()

def get_solutions_by_category(db: Session, category: str, skip: int = 0, limit: int = 10):
    # Query to get solutions filtered by category
    return db.query(Solution).filter(Solution.category == category).offset(skip).limit(limit).all()

def create_solution(db: Session, solution: SolutionCreate):
    # Creating a new solution using the SQLAlchemy model
    db_solution = Solution(name=solution.name, description=solution.description, price=solution.price, category=solution.category)
    db.add(db_solution)
    db.commit()
    db.refresh(db_solution)
    return db_solution
