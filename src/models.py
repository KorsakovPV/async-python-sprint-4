# from models.base_model import Base as BaseModel
from sqlalchemy import (TIMESTAMP, VARCHAR, Column, ForeignKey, func, sql, text, UniqueConstraint,
                        BOOLEAN, Boolean, Enum)
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import TIMESTAMP, VARCHAR, Column, ForeignKey, func, sql, text
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


# @as_declarative()
class BaseModel(Base):
    __abstract__ = True

    id: Column[UUID] = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text('uuid_generate_v4()'),
    )
    created_at = Column(TIMESTAMP(timezone=True), server_default=sql.func.current_timestamp())
    created_by = Column(String(255), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.current_timestamp())
    updated_by = Column(String(255), nullable=True)

    # @declared_attr
    # def __tablename__(cls):  # noqa 805
    #     return cls.__name__.lower()


class UrlModel(BaseModel):
    __tablename__ = 'urls'

    url = Column(String(), nullable=False, unique=True)
    is_delete = Column(Boolean, nullable=False, default=False)
    # history = relationship('HistoryModel', backref='url_history')  # type: ignore


class HistoryModel(BaseModel):
    __tablename__ = 'history'

    url_id = Column(
        UUID(as_uuid=True),
        ForeignKey('urls.id', ondelete='RESTRICT'),
        nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=True
    )
    domen = Column(String(), nullable=False)
    method = Column(Enum('GET', 'POST', 'PATCH', 'DELETE', name='request_methods'))


class UserModel(BaseModel):
    __tablename__ = 'users'

    name = Column(VARCHAR(255), nullable=False)
    # history = relationship('HistoryModel', backref='user_history')  # type: ignore
