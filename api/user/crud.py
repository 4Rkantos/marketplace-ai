from sqlalchemy.orm import Session
from models.user import User  # Modelo SQLAlchemy
from models.user import UserCreate  # Modelo Pydantic para criação

def get_user(db: Session, user_id: int):
    # Consulta usando o modelo SQLAlchemy
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    # Consulta usando o modelo SQLAlchemy
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    # Criando um novo usuário usando o modelo SQLAlchemy
    db_user = User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
