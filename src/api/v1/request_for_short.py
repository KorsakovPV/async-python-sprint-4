from fastapi import APIRouter, Depends

from db.db import get_session
from services.url_service import request_crud

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/{url_id:str}', response_model=None)
async def get_request(url_id: UUID, user_id: UUID | None = None,
                      db: AsyncSession = Depends(get_session)):
    return await request_crud.get(url_id=url_id, user_id=user_id, db=db)


@router.post('/{url_id:str}', response_model=None)
async def post_request(url_id: UUID, user_id: UUID | None = None,
                       db: AsyncSession = Depends(get_session)):
    return await request_crud.create(url_id=url_id, user_id=user_id, db=db)


@router.patch('/{url_id:str}', response_model=None)
async def patch_request(url_id: UUID, user_id: UUID | None = None,
                        db: AsyncSession = Depends(get_session)):
    return await request_crud.update(url_id=url_id, user_id=user_id, db=db)


@router.delete('/{url_id:str}', response_model=None)
async def delete_request(url_id: UUID, user_id: UUID | None = None,
                         db: AsyncSession = Depends(get_session)):
    return await request_crud.delete(url_id=url_id, user_id=user_id, db=db)
