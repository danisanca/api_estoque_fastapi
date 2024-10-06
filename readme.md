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


## Cofigurando o alembic para migrations do banco
- Com o alembic instalado (" pip install alembic ")
- Na raiz do projeto usar o comando (" alembic init alembic "), isso irá criar uma pasta do alembic e um arquivo de config "alembic.ini" na raiz do projeto.
### Configuração do arquivo alembic.ini
 - Adicione a seguinte linha de codigo após a variavel "version_path_separator":
 * sqlalchemy.url = postgresql://userdb:senha@localhost:5432/db_name

### Configuração a pasta alembic(Arquivo env)
- Import as lib's
 * import os
 * from dotenv import load_dotenv
 * import sys
### Configurando o banco de dados conforme o passo a passo a seguir:
#### Arquivo Modelo:
  *# this is the Alembic Config object, which provides
  *# access to the values within the .ini file in use.
  config = context.config

  *## Configurando o db para o alembic ------
  *# Passo 1: Adiciona a pasta 'scripts' ao sys.path
  sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

  *# Passo 2: Agora você pode importar o backup.py ou outros scripts dentro da pasta 'scripts'
  load_dotenv()

  *# Passo 3: Criando a url do banco de dados.
  URL_DATABASE = f'{os.getenv("DB_ENGINE")}://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

  *# Interpret the config file for Python logging.
  *# This line sets up loggers basically.
  if config.config_file_name is not None:
      fileConfig(config.config_file_name)

  *# add your model's MetaData object here
  *# Passo 4: Importando o model (Não mover esse import) 
  from src.models import BASE
  *# for 'autogenerate' support
  *# Passo 5: Aponta os metadata associados ao Base.
  target_metadata = BASE.metadata
  *# Passo 6: Definição do esquema do banco
  target_metadata.schema = os.environ.get("DB_SCHEMA")
  *# Passo 7: Configurando a URL de conexão
  config.set_main_option("sqlalchemy.url", URL_DATABASE)

  *# other values from the config, defined by the needs of env.py,
  *# can be acquired:
  *# my_important_option = config.get_main_option("my_important_option")
  *# ... etc.

### Trabalhando com as migration

#### Criando as migration do banco.
- O comando abaixo verifica os dados que estao no modelo e compara com o banco de dados, depois da analise ele cria um arquivo de migration com os dados que nao estao no banco de acordo com seu model:
 * alembic revision --autogenerate -m "First Commit"
- Para aplicar o arquivo de migração utilizar o comando abaixo:
 * alembic upgrade head
#### Criando uma Nova Migração Manual
- Para criar uma nova migração vazia para que seja apontado as alterações manuais no banco, execute o comando abaixo, substituindo `<mensagem_da_migracao>` por uma descrição da migração:
 * alembic revision -m "<mensagem_da_migracao>"
- Para aplicar a alteração criada usar o comando abaixo:
 * Usar o comando alembic upgrade head

## Em breve.
 - Integração com git Workflow para testes 
 - Docker para virtualização do banco + Api para app Mobile.