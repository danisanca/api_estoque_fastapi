from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from src import models,schemas
from typing import List
from src.utils import security
import uuid

class UsersRepository(ABC):
    @abstractmethod
    def create_user(self, data_create_user: schemas.UserCreate):
        raise NotImplementedError
    
    @abstractmethod
    def get_user_by_email(self, email: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_user_by_id(self, uid: str):
        raise NotImplementedError
    
    @abstractmethod
    def update_user_by_id(self, uid: str, body: schemas.users.UserUpdate):
        raise NotImplementedError
    
class UsersRepositorySQLAlchemy(UsersRepository):
    def __init__(self,db:Session) -> None:
        self.db:Session = db
    
    def create_user(self, data_create_user: schemas.UserCreate):
        # Gera um ID único para o novo usuário.
        id = str(uuid.uuid4())

        # Converte os dados de entrada do usuário para um formato manipulável (dicionário).
        data = data_create_user.model_dump()

        # Remove a senha do dicionário de dados e a armazena separadamente.
        password = data.pop("password")

        # Gera um 'salt' aleatório para ser usado na criação do hash da senha.
        salt = security.generate_salt()

        # Cria um hash da senha utilizando a senha fornecida e o salt gerado.
        hash_password = security.create_password_hash(password, salt)

        # Cria um modelo de usuário com os dados fornecidos e a senha hash.
        db_model = models.Users(**data, id=id, password=hash_password)

        # Adiciona o modelo de usuário à sessão do banco de dados.
        self.db.add(db_model)

        # Confirma a transação no banco de dados, salvando o novo usuário.
        self.db.commit()

        # Retorna o ID do usuário criado.
        return id

    def get_user_by_email(self, email: str):
        # Busca e retorna o primeiro usuário cujo e-mail corresponde ao fornecido.
        # Retorna None se nenhum usuário for encontrado.
        return self.db.query(models.Users).filter(models.Users.email == email).first()

    def get_user_by_id(self, uid: str):
        # Busca e retorna o usuário cujo ID corresponde ao fornecido.
        # Retorna None se nenhum usuário for encontrado.
        return self.db.query(models.Users).filter(models.Users.id == uid).first()

    def update_user_by_id(self, uid: str, body: schemas.users.UserUpdate):
        # Converte os dados recebidos do corpo da requisição para um dicionário.
        # A opção `exclude_none=True` garante que apenas os campos fornecidos
        # (ou seja, não nulos) sejam incluídos no dicionário.
        data = body.model_dump(exclude_none=True)

        # Executa uma consulta no banco de dados para localizar o usuário pelo ID