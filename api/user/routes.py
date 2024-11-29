from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud
from ...models import user
from ...database.config import Base, engine, get_db

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/user/", response_model=user.UserResponse)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=user.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user

@app.get("/users/", response_model=list[user.UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users