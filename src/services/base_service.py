from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Base


class BaseService:

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    async def create(self, *args, **kwargs):
        raise NotImplementedError

    async def update(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
        raise NotImplementedError


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseServiceDB(BaseService):

    def __init__(self, model: Type[ModelType]):
        self._model = model


class ReadServiceMixin(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    async def get(self, db: AsyncSession, id: UUID) -> Optional[ModelType]:
        statement = select(self._model).filter(self._model.id == id)  # type: ignore
        statement = await self.check_and_remove_is_delete(statement)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def check_and_remove_is_delete(self, statement):
        if hasattr(self._model, 'is_delete'):  # type: ignore
            statement = statement.filter(self._model.is_delete == False)  # type: ignore
        return statement

    async def get_multi(
            self, db: AsyncSession, *, skip=0, limit=100
    ) -> List[ModelType]:
        statement = select(self._model).offset(skip).limit(limit)  # type: ignore
        statement = await self.check_and_remove_is_delete(statement)
        results = await db.execute(statement=statement)
        return results.scalars().all()


class CreateServiceMixin(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_multi(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> List[ModelType]:
        objs_in_data = jsonable_encoder(obj_in)
        db_objs = [self._model(**obj_in_data) for obj_in_data in objs_in_data]  # type: ignore
        db.add_all(db_objs)
        await db.commit()
        for db_obj in db_objs:
            await db.refresh(db_obj)
        return db_objs


class UpdateServiceMixin(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        for key, value in obj_in:  # type: ignore
            setattr(db_obj, key, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


class DeleteServiceMixin(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    async def delete(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
    ) -> ModelType:
        setattr(db_obj, 'is_delete', True)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


class ServiceDB(
    ReadServiceMixin,
    CreateServiceMixin,
    UpdateServiceMixin,
    DeleteServiceMixin,
    BaseServiceDB,
    Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    pass


class ServiceDBReadOnly(
    ReadServiceMixin,
    BaseServiceDB,
    Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    pass
