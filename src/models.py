from .depends.database import BASE
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, TIMESTAMP, FLOAT,ForeignKey,Integer,BOOLEAN
from sqlalchemy.orm import relationship
import uuid,os

class Serializer:
    def dict(self):
        output = {}
        for k,v in self.__dict__.items():
            if k.startswith('_'):continue
            if isinstance(v,datetime):
                output[k] = str(v)
            elif isinstance(v,uuid.UUID):
                output[k] = str(v)
            elif isinstance(v,Serializer):
                output[k] = v.model_dump()
            elif isinstance(v,BASE):
                output[k] = v.model_dump()
            else:
                output[k] = v
        return output
    def model_dump(self):
        output = {}
        for k,v in self.__dict__.items():
            if k.startswith('_'):continue
            if isinstance(v,datetime):
                output[k] = str(v)
            elif isinstance(v,uuid.UUID):
                output[k] = str(v)
            elif isinstance(v,Serializer):
                output[k] = v.model_dump()
            elif isinstance(v,BASE):
                output[k] = v.model_dump()
            else:
                output[k] = v
        return output
    

class Users(BASE,Serializer):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(72), nullable=False)
    email = Column(String(82), nullable=False)
    password = Column(String(255), nullable=False)
    status = Column(String(32), nullable=False)
    role = Column(String(32), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.now(), onupdate=datetime.now())

