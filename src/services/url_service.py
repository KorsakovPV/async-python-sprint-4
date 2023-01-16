from uuid import UUID

# import aiohttp
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import HistoryModel, UrlModel
from schemes.urls_scheme import UrlCreateSchema, UrlEditSchema

from .base_service import BaseService, ServiceDB


class UrlServiceDB(ServiceDB[UrlModel, UrlCreateSchema, UrlEditSchema]):
    pass


url_crud = UrlServiceDB(UrlModel)


class RequestService(BaseService):

    async def check_and_remove_is_delete(self, statement):
        return statement.filter(UrlModel.is_delete == False)

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

    # async def get(self, url_id: UUID, user_id: UUID | None, db: AsyncSession):
    #     if url := await self.get_url_from_db_by_id(db, url_id):
    #         async with aiohttp.ClientSession() as session:
    #             async with session.get(url) as response:
    #                 response_json = await response.json()
    #         await self.add_in_history(user_id, url_id, db, method='GET')
    #         return response_json
    #     return {}
    #
    # async def create(self, url_id: UUID, user_id: UUID | None, db: AsyncSession):
    #     if url := await self.get_url_from_db_by_id(db, url_id):
    #         async with aiohttp.ClientSession() as session:
    #             async with session.post(url) as response:
    #                 response_json = await response.json()
    #         await self.add_in_history(user_id, url_id, db, method='GET')
    #         return response_json
    #     return {}
    #
    # async def update(self, url_id: UUID, user_id: UUID | None, db: AsyncSession):
    #     if url := await self.get_url_from_db_by_id(db, url_id):
    #         async with aiohttp.ClientSession() as session:
    #             async with session.patch(url) as response:
    #                 response_json = await response.json()
    #         await self.add_in_history(user_id, url_id, db, method='GET')
    #         return response_json
    #     return {}
    #
    # async def delete(self, url_id: UUID, user_id: UUID | None, db: AsyncSession):
    #     if url := await self.get_url_from_db_by_id(db, url_id):
    #         async with aiohttp.ClientSession() as session:
    #             async with session.delete(url) as response:
    #                 response_json = await response.json()
    #         await self.add_in_history(user_id, url_id, db, method='GET')
    #         return response_json
    #     return {}


request_crud = RequestService()
