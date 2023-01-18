from uuid import UUID
from starlette.requests import Request
from fastapi import Depends, FastAPI, Header, HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse, Response

from db.db import get_session
from services.request_service import request_crud

router = APIRouter()


@router.get('/{url_id:str}', response_class=Response)
async def get_request(
        url_id: UUID,
        request: Request,
        host: str = Header(),
        user_id: UUID | None = None,
        db: AsyncSession = Depends(get_session)
) -> RedirectResponse:
    url = await request_crud.custom_request(
        url_id=url_id,
        user_id=user_id,
        db=db,
        method=request.method,
        host=host
    )
    return RedirectResponse(url=url)


@router.post('/{url_id:str}', response_class=Response)
async def post_request(
        url_id: UUID,
        request: Request,
        host: str = Header(),
        user_id: UUID | None = None,
        db: AsyncSession = Depends(get_session)
) -> RedirectResponse:
    url = await request_crud.custom_request(
        url_id=url_id,
        user_id=user_id,
        db=db,
        method=request.method,
        host=host
    )
    return RedirectResponse(url=url)


@router.patch('/{url_id:str}', response_class=Response)
async def patch_request(
        url_id: UUID,
        request: Request,
        host: str = Header(),
        user_id: UUID | None = None,
        db: AsyncSession = Depends(get_session)
) -> RedirectResponse:
    url = await request_crud.custom_request(
        url_id=url_id,
        user_id=user_id,
        db=db,
        method=request.method,
        host=host
    )
    return RedirectResponse(url=url)


@router.delete('/{url_id:str}', response_class=Response)
async def delete_request(
        url_id: UUID,
        request: Request,
        host: str = Header(),
        user_id: UUID | None = None,
        db: AsyncSession = Depends(get_session)
) -> RedirectResponse:
    url = await request_crud.custom_request(
        url_id=url_id,
        user_id=user_id,
        db=db,
        method=request.method,
        host=host
    )
    return RedirectResponse(url=url)
