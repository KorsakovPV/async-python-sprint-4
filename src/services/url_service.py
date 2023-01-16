import httpx
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import HistoryModel

from models import UrlModel
from schemes.urls_scheme import UrlCreateSchema, UrlEditSchema
from .base_service import ServiceDB, BaseService


class UrlServiceDB(ServiceDB[UrlModel, UrlCreateSchema, UrlEditSchema]):
    pass


url_crud = UrlServiceDB(UrlModel)


class RequestService(BaseService):

    async def check_and_remove_is_delete(self, statement):
        return statement.filter(UrlModel.is_delete is False)

    async def add_in_history(self, user_id, url_id, db, method):
        db_obj = HistoryModel(
            url_id=url_id,
            user_id=user_id,
            # TODO прокинуть домен.
            domen='',
            method=method
        )
        db.add(db_obj)
        await db.commit()

    async def get_url_from_db_by_id(self, db, url_id):
        statement = select(UrlModel).filter(UrlModel.id == url_id)
        statement = await self.check_and_remove_is_delete(statement)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none().url

    # TODO Уточнить у наставника кок вернуть объект request а не json
    async def get(self, url_id: UUID, user_id: UUID | None, db: AsyncSession):
        if url := await self.get_url_from_db_by_id(db, url_id):
            async with httpx.AsyncClient() as client:
                proxy = await client.get(url)
            await self.add_in_history(user_id, url_id, db, method='GET')
            return proxy.json()
        return {}

    async def create(self, url_id: UUID, user_id: UUID | None, db: AsyncSession):
        if url := await self.get_url_from_db_by_id(db, url_id):
            async with httpx.AsyncClient() as client:
                proxy = await client.post(url)
            await self.add_in_history(user_id, url_id, db, method='POST')
            return proxy.json()
        return {}

    async def update(self, url_id: UUID, user_id: UUID | None, db: AsyncSession):
        if url := await self.get_url_from_db_by_id(db, url_id):
            async with httpx.AsyncClient() as client:
                proxy = await client.patch(url)
            await self.add_in_history(user_id, url_id, db, method='PATCH')
            return proxy.json()
        return {}

    async def delete(self, url_id: UUID, user_id: UUID | None, db: AsyncSession):
        if url := await self.get_url_from_db_by_id(db, url_id):
            async with httpx.AsyncClient() as client:
                proxy = await client.delete(url)
            await self.add_in_history(user_id, url_id, db, method='DELETE')
            return proxy.json()
        return {}


request_crud = RequestService()


class HistoryServiceDB():

    async def get_multi(
            self,
            url_id: UUID | None,
            user_id: UUID | None,
            domen: str | None,
            method: str | None,
            db: AsyncSession,
            *,
            skip=0,
            limit=100
    ) -> List[HistoryModel]:
        statement = select(HistoryModel).offset(skip).limit(limit)
        if url_id:
            statement = statement.filter(HistoryModel.url_id == url_id)
        if user_id:
            statement = statement.filter(HistoryModel.user_id == user_id)
        if domen:
            statement = statement.filter(HistoryModel.domen == domen)
        if method:
            statement = statement.filter(HistoryModel.method == method)
        results = await db.execute(statement=statement)
        return results.scalars().all()
        pass


history_crud = HistoryServiceDB()
