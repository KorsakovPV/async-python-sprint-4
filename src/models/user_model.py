from models.base_model import BaseModel
from sqlalchemy import TIMESTAMP, VARCHAR, Column, ForeignKey, func, sql, text
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy.orm import declarative_base, sessionmaker


class UserModel(BaseModel):
    __tablename__ = 'users'

    name = Column(VARCHAR(255), nullable=False)
