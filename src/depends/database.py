from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.pool import QueuePool

#os.getenv = Busca nas variaveis de ambiente,
#Concatena as configurações das variaveis de ambiente
url_default =  f'{os.getenv("DB_ENGINE")}://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
#Cria a url do banco
sqlalchemy_database_url =  os.getenv("DATABASE_URL", url_default)

#Engine cria a instancia do banco.
engine = create_engine(sqlalchemy_database_url,
                    poolclass=QueuePool,#Tipo de organização para tratar as requisiçoes
                    pool_size=10, # Tamanho maximo da fila
                    max_overflow=0,# Ele nao lembra depois eu que sou burro??
                    pool_recycle=1800,# Tempo da requisição dentro da fila.
                    connect_args={"connect_timeout": 10}  # Define um timeout para conexão dos que estao fora da conexao
                    )

#Criando uma sessão assincrona.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Criando uma classe base para os modelos ORM
BASE = declarative_base()

#Buscando a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
    finally:
        db.close()

# A função abaixo valida se todas as variaveis de ambiente foram criadas. caso o nao ele quebra e retorna a variavel faltante.
def validation_env(test=False):
    requires_env = ['DB_SCHEMA','DB_ENGINE','DB_USER','DB_PASSWORD',"DB_HOST","DB_PORT","DB_NAME"]
    requires = ['SECRET_KEY_JWT','ALGORITHM']
    #Se teste = True, não precisa validar nada
    if test and os.environ.get('DATABASE_URL_TEST',False):
        return

    #Validando as variaveis para criação do banco    
    for required in requires:
        if not  os.environ.get(required):
            msg =f'{required} is required in .env'
            raise RuntimeError(msg)
    #Validando as variaveis de configuração do jwt
    for required in requires_env:
        required=required+'_TEST' if test else required
        if not  os.environ.get(required):
            msg =f'{required} is required in .env'
            raise RuntimeError(msg)