from sqlalchemy import TIMESTAMP, VARCHAR, Column, ForeignKey, func, sql, text
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, relationship

from db.db import Base


# @as_declarative()
class BaseModel(Base):
    id: Column[UUID] = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text('uuid_generate_v4()'),
    )

    created_at = Column(TIMESTAMP(timezone=True), server_default=sql.func.current_timestamp())
    created_by = Column(VARCHAR(255), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.current_timestamp())
    updated_by = Column(VARCHAR(255), nullable=True)

    # @declared_attr
    # def __tablename__(cls):  # noqa 805
    #     return cls.__name__.lower()


class Entity(BaseModel):
    __tablename__ = "entity"
    # id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    # created_at = Column(DateTime, index=True, default=datetime.utcnow)
