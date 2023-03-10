import uuid

from sqlalchemy import (TIMESTAMP, VARCHAR, Boolean, Column, Enum, ForeignKey,
                        String, func, sql, text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base  # type: ignore

Base = declarative_base()


class BaseModel(Base):  # type: ignore
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    created_at = Column(TIMESTAMP(timezone=True), server_default=sql.func.current_timestamp())
    created_by = Column(String(255), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.current_timestamp())
    updated_by = Column(String(255), nullable=True)


class UrlModel(BaseModel):
    __tablename__ = 'urls'

    url = Column(String(255), nullable=False, unique=True)
    is_delete = Column(Boolean, nullable=False, default=False)


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
    domen = Column(String(255), nullable=False)
    method = Column(Enum('GET', 'POST', 'PATCH', 'DELETE', name='request_methods'))


class UserModel(BaseModel):
    __tablename__ = 'users'

    name = Column(VARCHAR(255), nullable=False)
