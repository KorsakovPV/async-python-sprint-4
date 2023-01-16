from pydantic import BaseModel
from pydantic.json import UUID

from schemes.base_scheme import (BaseCreateSchema, BaseEditSchema,
                                 BaseReadSchema)


class HistoryBaseSchema(BaseModel):
    url_id: UUID | None
    user_id: UUID | None
    domen: str | None
    method: str | None


class HistoryReadSchema(HistoryBaseSchema, BaseReadSchema):
    pass


class HistoryCreateSchema(HistoryBaseSchema, BaseCreateSchema):
    pass


class HistoryEditSchema(HistoryBaseSchema, BaseEditSchema):
    pass
