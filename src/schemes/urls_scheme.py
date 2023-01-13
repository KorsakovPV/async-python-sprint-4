from schemes.base_scheme import BaseReadSchema, BaseCreateSchema, BaseEditSchema

from pydantic import BaseModel


class UrlBaseSchema(BaseModel):
    url: str
    is_delete: bool


class UrlReadSchema(UrlBaseSchema, BaseReadSchema):
    pass


class UrlCreateSchema(UrlBaseSchema, BaseCreateSchema):
    pass


class UrlEditSchema(UrlBaseSchema, BaseEditSchema):
    pass
