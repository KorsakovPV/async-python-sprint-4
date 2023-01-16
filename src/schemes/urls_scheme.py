from schemes.base_scheme import BaseReadSchema, BaseCreateSchema, BaseEditSchema

from pydantic import BaseModel


class UrlBaseSchema(BaseModel):
    url: str


class UrlReadSchema(UrlBaseSchema, BaseReadSchema):
    is_delete: bool


class UrlCreateSchema(UrlBaseSchema, BaseCreateSchema):
    pass


class UrlEditSchema(UrlBaseSchema, BaseEditSchema):
    pass
