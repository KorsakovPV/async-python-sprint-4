from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse, Response

from db.db import get_session
from services.url_service import request_crud

router = APIRouter()


@router.get('/{url_id:str}', response_class=Response)
async def get_request(url_id: UUID, user_id: UUID | None = None,
                      db: AsyncSession = Depends(get_session)):
    url = await request_crud.custom_request(url_id=url_id, user_id=user_id, db=db, method='GET')
    return RedirectResponse(url=url)


@router.post('/{url_id:str}', response_class=Response)
async def post_request(url_id: UUID, user_id: UUID | None = None,
                       db: AsyncSession = Depends(get_session)):
    url = await request_crud.custom_request(url_id=url_id, user_id=user_id, db=db, method='POST')
    return RedirectResponse(url=url)


@router.patch('/{url_id:str}', response_class=Response)
async def patch_request(url_id: UUID, user_id: UUID | None = None,
                        db: AsyncSession = Depends(get_session)):
    url = await request_crud.custom_request(url_id=url_id, user_id=user_id, db=db, method='PATCH')
    return RedirectResponse(url=url)


@router.delete('/{url_id:str}', response_class=Response)
async def delete_request(url_id: UUID, user_id: UUID | None = None,
                         db: AsyncSession = Depends(get_session)):
    url = await request_crud.custom_request(
        url_id=url_id, user_id=user_id, db=db, method='DELETE'
    )
    return RedirectResponse(url=url)
