import sys

from fastapi import APIRouter, Depends
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette import status

from api.v1 import history, request_for_short, url
from db.db import get_session

api_router = APIRouter()
api_router.include_router(url.router, prefix="/urls", tags=['urls'])
api_router.include_router(history.router, prefix="/history", tags=['history'])
api_router.include_router(request_for_short.router, prefix="/request", tags=['request'])


@api_router.get('/', status_code=status.HTTP_200_OK)
async def root_handler():
    return {'version': 'v1'}


@api_router.get('/ping', status_code=status.HTTP_200_OK)
async def ping_db(db: Session = Depends(get_session)):
    sql = 'SELECT version();'
    try:
        result = await db.execute(sql)
        ver_db, = [x for x in result.scalars()]
        return {
            'api': 'v1',
            'python': sys.version_info,
            'db': ver_db
        }
    except exc.SQLAlchemyError:
        return {
            'api': 'v1',
            'python': sys.version_info,
            'db': 'not available'
        }
