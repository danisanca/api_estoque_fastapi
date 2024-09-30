from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.depends.database import get_db
import os
##--
from src.utils.errors import error_internal_server
from src import crud,schemas

# Buscando as Configurações do JWT
SECRET_KEY = os.environ.get("SECRET_KEY_JWT")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", '30'))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", '400'))

#Cria o tipo de hashing da senha que será salva no banco
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#Definição da autenticação do Bearer pela rota /token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Criando token de autenticação
def create_access_token(uid:str, expires_delta: Optional[timedelta] = None,data={}):
    ##Verifica se o conteudo de data é um dicionario. Data utilizado para passar insformaçoes adicionais dentro do token
    if not isinstance(data,dict):
        raise error_internal_server(msg="function create_access_token data must be a dict")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire,**to_encode,'uid':uid})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

#Buscando o usuario que está logado
async def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: str = payload.get("uid")
        if uid is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    except:
        raise credentials_exception
    user = crud.users.get_user_by_id(uid,db)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: schemas.users.User = Depends(get_current_user)):
    return current_user