from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from models.user import User
from passlib.context import CryptContext
from jose import JWTError, jwt
from database.config import get_db
from datetime import datetime, timedelta


SECRET_KEY = "secret"
ALGORITHM = "HS256"


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


#Recebe o token como um Bearer Token no cabeçalho da requisição.
def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # O token estará no cabeçalho 'Authorization' no formato "Bearer <token>"
        token = authorization.split(" ")[1]  # Separa "Bearer" do token real

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    except IndexError:
        raise credentials_exception
    return user


#Cria um token JWT para autenticação.
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    to_encode = data.copy()  # Fazemos uma cópia dos dados fornecidos
    expire = datetime.utcnow() + expires_delta  # Define o tempo de expiração
    to_encode.update({"exp": expire})  # Adiciona o campo de expiração aos dados
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Codifica o JWT
    return encoded_jwt


def is_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Esta rota é restrita a administradores.",
        )
    return current_user
