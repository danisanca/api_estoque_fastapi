from sqlalchemy.orm import Session
from src import schemas,models
from src.utils import security
import uuid

def create_user(data_create_user: schemas.UserCreate, db: Session):
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
    db.add(db_model)

    # Confirma a transação no banco de dados, salvando o novo usuário.
    db.commit()

    # Retorna o ID do usuário criado.
    return id

def get_user_by_id(uid: str, db: Session):
    # Busca e retorna o usuário cujo ID corresponde ao fornecido.
    # Retorna None se nenhum usuário for encontrado.
    return db.query(models.Users).filter(models.Users.id == uid).first()

def update_user_by_id(uid: str, body: schemas.users.UserUpdate, db: Session):
    # Converte os dados recebidos do corpo da requisição para um dicionário.
    # A opção `exclude_none=True` garante que apenas os campos fornecidos
    # (ou seja, não nulos) sejam incluídos no dicionário.
    data = body.model_dump(exclude_none=True)

    # Executa uma consulta no banco de dados para localizar o usuário pelo ID fornecido.
    # Em seguida, atualiza o usuário com os dados fornecidos.
    # Esta ação não retorna nenhum objeto; ela apenas prepara a consulta para ser executada.
    db.query(models.Users).filter(models.Users.id == uid).update(data)

    # Efetua o commit da transação, aplicando as atualizações no banco de dados.
    db.commit()

def get_user_by_email(email: str, db: Session):
    # Busca e retorna o primeiro usuário cujo e-mail corresponde ao fornecido.
    # Retorna None se nenhum usuário for encontrado.
    return db.query(models.Users).filter(models.Users.email == email).first()