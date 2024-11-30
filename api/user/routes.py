from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.user import crud
from models.user import UserCreate, UserResponse, UserLogin  # Modelos Pydantic
from database.config import Base, engine, get_db
from pydantic import ValidationError

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

router = APIRouter()

# Criar novo usuário
@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Verifique se a criação do usuário foi bem-sucedida
        return crud.create_user(db=db, user=user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro na criação do usuário: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")
    

# Realiza o login do usuário
@router.post("/users/login/", response_model=UserResponse)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    try:
        user = crud.authenticate_user(db, email=credentials.email, password=credentials.password)
        if not user:
            raise HTTPException(status_code=401, detail="Credenciais inválidas.")
        return user
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Dados inválidos para o login.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")



# Busca usuário por ID
@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try: 
        db_user = crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        return db_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")

# Busca todos os usuários cadastrados
@router.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return crud.get_users(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")
