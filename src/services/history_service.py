from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import HistoryModel


class HistoryServiceDB:

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
            statement = statement.filter(HistoryModel.url_id == url_id)  # type: ignore
        if user_id:
            statement = statement.filter(HistoryModel.user_id == user_id)  # type: ignore
        if domen:
            statement = statement.filter(HistoryModel.domen == domen)  # type: ignore
        if method:
            statement = statement.filter(HistoryModel.method == method)  # type: ignore
        results = await db.execute(statement=statement)
        return results.scalars().all()


history_crud = HistoryServiceDB()
