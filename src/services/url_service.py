from models import UrlModel
from schemes.urls_scheme import UrlCreateSchema, UrlEditSchema
from .base_service import ServiceDB


class UrlServiceDB(ServiceDB[UrlModel, UrlCreateSchema, UrlEditSchema]):
    pass


url_crud = UrlServiceDB(UrlModel)
