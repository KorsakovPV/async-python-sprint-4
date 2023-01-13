import uvicorn
from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from api.v1 import base
from config.config import settings
from config.logger import logger

import time

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

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

if __name__ == '__main__':
    logger.info(f'Server started.')
    uvicorn.run(
        'main:app',
        host=settings.API_HOST,
        port=settings.API_PORT,
    )
