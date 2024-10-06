from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
#Meus Imports

import os
from dotenv import load_dotenv
import sys

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

## Configurando o db para o alembic ------
# Passo 1: Adiciona a pasta 'scripts' ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

# Passo 2: Agora você pode importar o backup.py ou outros scripts dentro da pasta 'scripts'
load_dotenv()

# Passo 3: Criando a url do banco de dados.
URL_DATABASE = f'{os.getenv("DB_ENGINE")}://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# Passo 4: Importando o model (Não mover esse import) 
from src.models import BASE
# for 'autogenerate' support
# Passo 5: Aponta os metadata associados ao Base.
target_metadata = BASE.metadata
# Passo 6: Definição do esquema do banco
target_metadata.schema = os.environ.get("DB_SCHEMA")
# Passo 7: Configurando a URL de conexão
config.set_main_option("sqlalchemy.url", URL_DATABASE)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
