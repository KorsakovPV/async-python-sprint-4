import sys

from fastapi import APIRouter

# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get('/')
async def root_handler():
    return {'version': 'v1'}


@router.get('/info')
async def info_handler():
    return {
        'api': 'v1',
        'python': sys.version_info
    }
