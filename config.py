from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
load_dotenv()

# Configurações do Banco de Dados
DATABASE_URL = "postgresql://joao_silva:123@localhost/marketplaceiadb"
#os.getenv("DATABASE_URL")

# Configurações de E-mail
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))  # Porta padrão como fallback
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
