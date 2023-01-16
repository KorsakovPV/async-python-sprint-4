from pydantic import BaseModel

from schemes.base_scheme import (BaseCreateSchema, BaseEditSchema,
                                 BaseReadSchema)


class UrlBaseSchema(BaseModel):
    url: str


class UrlReadSchema(UrlBaseSchema, BaseReadSchema):
    is_delete: bool


class UrlCreateSchema(UrlBaseSchema, BaseCreateSchema):
    pass


class UrlEditSchema(UrlBaseSchema, BaseEditSchema):
    pass
