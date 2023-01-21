from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from db.db import get_session
from services.request_service import request_crud

router = APIRouter()


@router.get('/{url_id:str}', response_class=Response)
async def get_request(
        url_id: UUID,
        request: Request,
        user_id: UUID | None = None,
        db: AsyncSession = Depends(get_session)
) -> RedirectResponse:
    url = await request_crud.custom_request(
        url_id=url_id,
        user_id=user_id,
        db=db,
        method=request.method,
        host=request.headers.get("host", "").split(":")[0]
    )
    return RedirectResponse(url=url)
