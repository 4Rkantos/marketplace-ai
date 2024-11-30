from sqlalchemy.orm import Session
from models.user import User  # Modelo SQLAlchemy
from models.user import UserCreate  # Modelo Pydantic para criação
from api.utils.utils import get_password_hash, get_user_by_email, verify_password

#Busca usuário por ID
def get_user(db: Session, user_id: int):
    # Consulta usando o modelo SQLAlchemy
    return db.query(User).filter(User.id == user_id).first()

#Busca todos os usuários, com limite de 10
def get_users(db: Session, skip: int = 0, limit: int = 10):
    # Consulta usando o modelo SQLAlchemy
    return db.query(User).offset(skip).limit(limit).all()

#Cria um novo usuário
def create_user(db: Session, user: UserCreate, is_admin: bool = False):
    if get_user_by_email(db, user.email):
        raise ValueError("Email já cadastrado.")
    
    # Cria o hash da senha
    hashed_password = get_password_hash(user.password)

    # Atualiza o banco de dados com o novo usuário
    db_user = User(
        name=user.name, 
        email=user.email, 
        password=hashed_password, 
        is_admin=user.is_admin
    )
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