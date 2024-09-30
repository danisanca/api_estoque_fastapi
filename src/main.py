from dotenv import load_dotenv
from sqlalchemy.orm import Session
load_dotenv()
from fastapi import FastAPI,HTTPException,Depends
from src import routes
from src import crud,utils,depends
from src.depends.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from src import models,depends
from contextlib import asynccontextmanager

# - Validando as variaveis de ambiente
try:
    depends.database.validation_env()
except RuntimeError as e:
    exit(str(e))

# - Veiricando os modelos do banco de dados se estão criados antes de executar a api
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    #models.BASE.metadata.drop_all(depends.database.engine)
    models.BASE.metadata.create_all(depends.database.engine,checkfirst=True)
    #
    yield
    
    # Clean up the ML models and release the resources

# - Configuração Inicial da api
app = FastAPI(
    lifespan=lifespan
)
# - Configuração do CORS
app.add_middleware(
    
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens. Você pode restringir para domínios específicos.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos.
)

# - Apontando as rotas criadas
app.include_router(routes.users.router)

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """
    Este endpoint `/token` é utilizado para autenticar usuários e gerar um token de acesso (JWT). O processo de autenticação ocorre da seguinte forma:

        1. **Recebimento dos Dados de Login:** O endpoint aceita dados de login através de um formulário padrão OAuth2 (`OAuth2PasswordRequestForm`), que inclui o nome de usuário (username) e a senha (password).

        2. **Verificação do Usuário:** Utiliza a função `crud.users.get_user_by_email` para buscar o usuário pelo e-mail fornecido (`form_data.username`). Se o usuário não for encontrado, levanta uma exceção HTTP com status 400 e a mensagem "Username or password incorrect".

        3. **Verificação de Senha:** Caso o usuário seja encontrado, verifica se a senha fornecida corresponde à senha armazenada no banco de dados. Isso é feito através da função `utils.security.verify_password`. Se a senha estiver incorreta, a mesma exceção do passo anterior é levantada.

        4. **Geração do Token de Acesso:** Se as credenciais estiverem corretas, um token de acesso JWT é gerado usando `depends.jwt.create_access_token`, com o ID do usuário como payload.

        5. **Retorno do Token:** Retorna um objeto JSON contendo o `access_token` e o tipo de token (`bearer`).

        Este endpoint é fundamental para o processo de login, permitindo aos usuários autenticar suas credenciais e receber um token JWT para acessar outros endpoints protegidos no sistema.
    """
    user_dict = crud.users.get_user_by_email(form_data.username,db)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not utils.security.verify_password(form_data.password, user_dict.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = depends.jwt.create_access_token(uid= str(user_dict.id))

    return {"access_token": access_token, "token_type": "bearer"}