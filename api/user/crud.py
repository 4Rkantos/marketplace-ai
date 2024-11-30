from sqlalchemy.orm import Session
from models.user import User  # Modelo SQLAlchemy
from models.user import UserCreate  # Modelo Pydantic para criação
from passlib.context import CryptContext

# 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funções auxiliares

#Gera um hash para a senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

#Verifica se a senha fornecida combina com o hash do banco
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#Busca usuário por e-mail
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

#Funções das APIs 
#Busca usuário por ID
def get_user(db: Session, user_id: int):
    # Consulta usando o modelo SQLAlchemy
    return db.query(User).filter(User.id == user_id).first()

#Busca todos os usuários, com limite de 10
def get_users(db: Session, skip: int = 0, limit: int = 10):
    # Consulta usando o modelo SQLAlchemy
    return db.query(User).offset(skip).limit(limit).all()

#Cria um novo usuário
def create_user(db: Session, user: UserCreate):
    if get_user_by_email(db, user.email):
        raise ValueError("Email já cadastrado.")
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Realiza o login
def authenticate_user(db: Session, email: str, password: str):
    try:
        user = get_user_by_email(db, email)
        if user and verify_password(password, user.password):
            return user
        return None
    except Exception as e:
        raise Exception(f"Erro ao autenticar o usuário: {str(e)}")