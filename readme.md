## Informações Basicas da Api
- Api criada com FastApi + SqlAlchemi
- Projeto utiliza o banco de dados Postgres
- Versão do python 3.10.11

## Config inicial
### Criar o ambiente virtual
  python3 -m venv .venv

### Se conectar no ambiente
  source .venv/Scripts/activate

### instalando as dependencia
  Após logar no ambiente usar: pip install -r requirements.txt

### Criar o arquivo .env
  Criar um arquivo .env na raiz do projeto com as variavies abaixo para conexão
  #### -- Config Dev
  DB_ENGINE=postgresql+psycopg2
  DB_USER=usuario do banco
  DB_PASSWORD=Senha do banco
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=Nome do banco
  DB_SCHEMA=public
  #### -Para Teste
  DB_ENGINE_TEST=postgresql+psycopg2
  DB_USER_TEST=usuario do banco
  DB_PASSWORD_TEST=Senha do banco
  DB_HOST_TEST=localhost
  DB_PORT_TEST=5433
  DB_NAME_TEST=Nome do banco
  DB_SCHEMA_TEST=public
  #### -Config JWT
  SECRET_KEY_JWT= Gerar token
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=30
  REFRESH_TOKEN_EXPIRE_MINUTES=400

### Como gerar um token
- criar um arquivo .ipynb ou rodar direto no terminar.
import secrets
token = secrets.token_urlsafe(32)
token

### Iniciar a aplicação em desenvolvimento
 uvicorn src.main:app --reload


