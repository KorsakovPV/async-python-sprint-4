import uvicorn
from fastapi import FastAPI, Depends
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.trustedhost import TrustedHostMiddleware

from api.v1 import base
from config.config import settings
from config.logger import logger

from fastapi_auth_middleware import AuthMiddleware

import time

from db.db import get_session
from middleware.blocked_host import BlockedHostMiddleware

# from config import config

# from core import config
# from core.logger import LOGGING

app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=settings.PROJECT_NAME,
    # Адрес документации в красивом интерфейсе
    # docs_url='/api/openapi',
    # Адрес документации в формате OpenAPI
    # openapi_url='/api/openapi.json',
    # Можно сразу сделать небольшую оптимизацию сервиса
    # и заменить стандартный JSON-сериализатор на более шуструю версию, написанную на Rust
    default_response_class=ORJSONResponse,
)

app.include_router(base.api_router, prefix='/api/v1')

app.add_middleware(
    BlockedHostMiddleware, blocked_hosts=['example.com', '*.example.com']
)

if __name__ == '__main__':
    logger.info(f'Server started.')
    uvicorn.run(
        'main:app',
        host=settings.API_HOST,
        port=settings.API_PORT,
    )
