
Passo A Passo.
## Config inicial
#### Criar o ambiente virtual
  python3 -m venv .venv
#### Se conectar no ambiente
  source .venv/Scripts/activate

## Iniciar a aplicação em desenvolvimento
 uvicorn src.main:app --reload

#### Instalar as dependencias
    fastapi
    psycopg2-binary - Se for usar postgree
    asyncpg  - Se for usar postgree
    aiomysql  - Se for usar o mysql
    sqlalchemy 
    uvicorn
    python-jose[cryptography]
    pytz
    passlib
    python-multipart
    pydantic[email]

## Config do Projeto

