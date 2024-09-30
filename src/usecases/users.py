from src import schemas,models
from src import repositories

class CreateUserUsecase:
    def __init__(self, repo:repositories.users.UsersRepository):
        self.repo = repo

    def execute(self, user:schemas.users.UserCreate, *args, **kwargs):
        return self.repo.create_user(user,*args,**kwargs)

class GetUserByEmailUsecase:
    def __init__(self, repo:repositories.users.UsersRepository):
        self.repo = repo

    def execute(self, email:str, *args,**kwargs):
        return self.repo.get_user_by_email(email,*args,**kwargs)

class GetUserByIdUsecase:
    def __init__(self, repo:repositories.users.UsersRepository):
        self.repo = repo

    def execute(self, uid:str, *args,**kwargs):
        return self.repo.get_user_by_id(uid,*args,**kwargs)

class UpdateUserByIdUsecase:
    def __init__(self, repo:repositories.users.UsersRepository):
        self.repo = repo

    def execute(self, uid:str, body:schemas.users.UserUpdate, *args,**kwargs):
        return self.repo.update_user_by_id(uid,body,*args,**kwargs)