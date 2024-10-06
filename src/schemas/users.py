from pydantic import BaseModel,ConfigDict,Field

class Token(BaseModel):
    access_token: str
    token_type:str="bearer"
    refresh_token: str
    
class UserBase(BaseModel):
    name: str=Field(min_length=3)
    email: str=Field(min_length=3)
    status: str = "Active"
    role: str
    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str=Field(min_length=8)
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(UserBase):
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=8)
    model_config = ConfigDict(from_attributes=True)