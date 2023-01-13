import sys

from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import exc

from api.v1 import url
from db.db import get_session

# Объект router, в котором регистрируем обработчики
api_router = APIRouter()
api_router.include_router(url.router, prefix="/urls", tags=["urls"])


@api_router.get('/')
async def root_handler():
    return {'version': 'v1'}


@api_router.get('/ping')
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
