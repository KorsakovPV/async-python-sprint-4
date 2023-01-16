from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from services.history_service import history_crud

router = APIRouter()


@router.get('/history', response_model=None)
async def get_status(
        url_id: UUID | None = None,
        user_id: UUID | None = None,
        domen: str | None = None,
        method: str | None = None,
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_session),
) -> Any:
    return await history_crud.get_multi(
        url_id=url_id,
        user_id=user_id,
        domen=domen,
        method=method,
        db=db,
        skip=skip,
        limit=limit
    )
