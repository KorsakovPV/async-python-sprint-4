from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseReadSchema(BaseModel):
    id: UUID

    created_at: datetime
    created_by: str | None
    updated_at: datetime | None
    updated_by: str | None

    class Config:
        orm_mode = True


class BaseCreateSchema(BaseModel):
    created_by: str | None


class BaseEditSchema(BaseModel):
    updated_by: str | None
