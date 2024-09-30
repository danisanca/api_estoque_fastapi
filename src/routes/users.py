from datetime import timedelta
from fastapi import APIRouter, Depends,status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.depends import database, jwt
from src.utils import errors
from src import schemas, crud, utils

router = APIRouter(prefix="/users", tags=["users"])


######################################
#                                    #
# - Rotas do Usuario                 #
#                                    #
######################################
@router.post("/create-user", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def create_user(data_create_user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    #Verifica se ja existe um e-mail cadastrado
    if crud.users.get_user_by_email(data_create_user.email, db) != None:
        raise errors.error_user_already_registered(loc=['email'])
    
    #Caso crio o usuario gera o token de acesso(`access_token`) e de atualização (`refresh_token`) usando JWT
    try:
        uid = crud.users.create_user(data_create_user, db)
        access_token = jwt.create_access_token(uid=uid)
        refresh_token = jwt.create_access_token(
            uid=uid, expires_delta=timedelta(minutes=jwt.REFRESH_TOKEN_EXPIRE_MINUTES))
        return schemas.Token(access_token=access_token, refresh_token=refresh_token)

    #Em caso de erro de integridade, rollback no banco de dados e trata o erro conforme necessário. 
    except IntegrityError as e:
        db.rollback()
        if 'unique constraint' in str(e.orig):
            print("Erro: Chave única violada.")
            # Trate o erro conforme necessário
        else:
            print("Outro erro de integridade ocorreu.")
            # Trate outros erros de integridade
        raise errors.error_user_already_registered(loc=['email'])
    #Em caso de outros erros, resulta em um rollback e levanta uma exceção genérica.
    except Exception as e:
        db.rollback()
        print("Ocorreu um erro inesperado:", e)
        raise errors.generic_error()
        # Trate outros tipos de exceções

#Rota retorna o usuario autenticado.
@router.get("/me", response_model=schemas.users.User)
def me(user: schemas.users.User = Depends(jwt.get_current_active_user)):
    #model.dump(), formata os dados antes do retorno
    return user.model_dump()

#Rota para atualização dos dados do usuario authenticado.
@router.put('/me/update',status_code=status.HTTP_201_CREATED)
def update_me_user(body:schemas.users.UserUpdate,user : schemas.users.User=Depends(jwt.get_current_active_user),db:Session=Depends(database.get_db)):
    crud.users.update_user_by_id(user.id,body,db)
    return 'ok'


######################################
#                                    #
# - Rotas de Login / Autenticação    #
#                                    #
######################################
@router.post("/login", response_model=schemas.Token)
def login(data_login: schemas.users.UserLogin, db: Session = Depends(database.get_db)):
    # Busca o usuario no banco pelo e-mail.
    user = crud.users.get_user_by_email(data_login.email, db)
    if user == None:
        raise errors.erro_not_found(msg="User not found", loc=['email'])
    #Verifica a senha no banco comparando a senha informada com a hash da senha salva
    if not utils.security.verify_password(data_login.password, user.password):
        raise errors.erro_unauthorized(
            loc=['password'], msg="Incorrect password")

    #Se ok com os dados cria o token e o refresh token
    access_token = jwt.create_access_token(uid=str(user.id))
    refresh_token = jwt.create_access_token(
            uid=str(user.id), expires_delta=timedelta(minutes=jwt.REFRESH_TOKEN_EXPIRE_MINUTES))

    #retorna o schemas token definido no schemas user que é só pra login
    return schemas.Token(access_token=access_token, refresh_token=refresh_token)

@router.get("/refresh", response_model=schemas.Token)
def refresh(user: schemas.users.User = Depends(jwt.get_current_active_user)):

    access_token = jwt.create_access_token(uid=str(user.id))
    refresh_token = jwt.create_access_token(
            uid=str(user.id), expires_delta=timedelta(minutes=jwt.REFRESH_TOKEN_EXPIRE_MINUTES))

    return schemas.Token(access_token=access_token, refresh_token=refresh_token)



