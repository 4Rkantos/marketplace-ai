from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.user.routes import app as user_router
from database.config import Base, engine

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicialização da aplicação FastAPI
app = FastAPI(
    title="Marketplace AI",
    description="API para gerenciamento de usuários e soluções de IA.",
    version="1.0.0",
)

# Configuração de CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost",
    "http://localhost:3000",  # Front-end local
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de roteadores
app.include_router(user_router, prefix="/api/users", tags=["Users"])

# Rota base para verificação
@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Marketplace AI!"}
