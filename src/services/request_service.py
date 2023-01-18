from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import HistoryModel, UrlModel


class RequestService:

    async def check_and_remove_is_delete(self, statement):
        return statement.filter(UrlModel.is_delete == False)  # noqa

    async def add_in_history(self, user_id, url_id, db, method, host):
        db_obj = HistoryModel(
            url_id=url_id,
            user_id=user_id,
            domen=host,
            method=method
        )
        db.add(db_obj)
        await db.commit()

    async def get_url_from_db_by_id(self, db, url_id):
        statement = select(UrlModel).filter(UrlModel.id == url_id)
        statement = await self.check_and_remove_is_delete(statement)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def custom_request(
            self,
            url_id: UUID,
            user_id: UUID | None,
            db: AsyncSession,
            method: str,
            host: str
    ):
        if url := await self.get_url_from_db_by_id(db, url_id):
            await self.add_in_history(user_id, url_id, db, method=method, host=host)
            return url.url
        raise HTTPException(status_code=404, detail="Item not found")


request_crud = RequestService()
