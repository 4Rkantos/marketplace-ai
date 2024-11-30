from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Request, HTTPException, status
from models.user import User

SECRET_KEY = "secret"
ALGORITHM = "HS256"

class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # Verifica se o token está presente no cabeçalho Authorization
        token = request.headers.get("Authorization")
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais não fornecidas. Certifique-se de incluir o cabeçalho 'Authorization: Bearer <token>'",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            # Extrai o token JWT do cabeçalho Authorization
            token = token.split(" ")[1]  # Pega apenas o token, que está no formato "Bearer token"
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciais inválidas",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Verifica se o usuário existe no banco
            db = Session()
            user = db.query(User).filter(User.email == email).first()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuário não encontrado",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            # Salva o usuário na requisição para usar nas rotas
            request.state.user = user
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token inválido: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        response = await call_next(request)
        return response
