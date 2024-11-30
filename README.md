# Marketplace AI

Um marketplace inovador que conecta usuários e empresas a soluções de Inteligência Artificial especializadas. Organiza e disponibiliza IAs para atender demandas específicas de diferentes setores.

## 🚀 Tecnologias Utilizadas
- Python 3.8.10
- FastAPI
- PostgreSQL
- SQLAlchemy
- Mailtrap
- Firebase (Hosting)

## 📁 Estrutura do Projeto
- **api/**: Contém a configuração das APIs e endpoints da aplicação, com as rotas principais que comunicam o backend com o frontend.
- **app/**: Código principal da aplicação, incluindo a lógica de negócios, manipulação de dados e interação entre as diferentes partes do sistema.
- **database/**: Configuração e modelos relacionados ao banco de dados, incluindo a inicialização da conexão e operações de CRUD.
- **models/**: Define os modelos de dados da aplicação, representando as principais entidades do sistema, como Usuário, Produtos, e demais objetos do marketplace.
- **utils/**: Contém utilitários gerais, como funções para envio de e-mails, manipulação de arquivos e outras funções auxiliares para o funcionamento do sistema.
- **.env**: Arquivo para variáveis de ambiente sensíveis, como configurações de banco de dados, credenciais de API e outras chaves secretas (não incluso no repositório para segurança).


## 🔧 Configuração do Ambiente

### Pré-requisitos
Certifique-se de ter instalado:
- [Python 3.8.10+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/downloads)

### Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/marketplace-ai.git
   cd marketplace-ai

2. Crie e ative um ambiente virtual:
   ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3. Instale as dependências:
   ```bash
    pip install -r requirements.txt

4. Configure o banco de dados:
   ```bash
    - No PostgreSQL, crie um banco chamado marketplace_ai.
    - Configure as credenciais no arquivo .env:
    DATABASE_URL="postgresql://<usuario>:<senha>@localhost:porta/marketplace_ai"
