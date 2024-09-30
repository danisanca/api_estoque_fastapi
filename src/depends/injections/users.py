from sqlalchemy.orm import Session
from src import repositories,usecases

def get_user_repository(db: Session ) -> repositories.users.UsersRepository:
    return repositories.users.UsersRepositorySQLAlchemy(db)

def get_create_user_usecase(db: Session ) -> usecases.users.CreateUserUsecase:
    return usecases.users.CreateUserUsecase(get_user_repository(db))

def get_get_user_by_email_usecase(db: Session ) -> usecases.users.GetUserByEmailUsecase:
    return usecases.users.GetUserByEmailUsecase(get_user_repository(db))

def get_get_user_by_id_usecase(db: Session ) -> usecases.users.GetUserByIdUsecase:
    return usecases.users.GetUserByIdUsecase(get_user_repository(db))

def get_update_user_by_id_usecase(db: Session ) -> usecases.users.UpdateUserByIdUsecase:
    return usecases.users.UpdateUserByIdUsecase(get_user_repository(db))