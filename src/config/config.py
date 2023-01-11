from typing import Any, Dict, Optional, Union
from logging import config as logging_config

from pydantic import BaseSettings, PostgresDsn, validator

# from config.logger import LOGGING

SENTRY_DSN_TEST = ''


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Async python sprint-4'

    DB_HOST: str = 'localhost'
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_NAME: str = 'async_python_sprint_4'
    DB_PORT: int = 5432
    DB_URL: Optional[Union[PostgresDsn, str]] = ''

    TEST_DB_HOST: str = 'localhost'
    TEST_DB_USER: str = 'postgres'
    TEST_DB_PASSWORD: str = 'postgres'
    TEST_DB_NAME: str = 'test_async_python_sprint_4'
    TEST_DB_PORT: int = 5432
    TEST_DB_URL: Optional[Union[PostgresDsn, str]] = ''

    API_HOST: str = '0.0.0.0'
    API_PORT: int = 8000

    @validator('DB_URL', pre=True)
    def assemble_db_connection(cls, value: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(value, str) and value != '':
            return value
        return PostgresDsn.build(  # type: ignore
            scheme='postgresql+asyncpg',
            user=values.get('DB_USER'),
            password=values.get('DB_PASSWORD'),
            host=values.get('DB_HOST'),
            port=str(values.get('DB_PORT')),
            path=f'/{values.get("DB_NAME") or ""}',
        )

    @validator('TEST_DB_URL', pre=True)
    def assemble_test_db_connection(cls, value: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(value, str) and value != '':
            return value
        return PostgresDsn.build(  # type: ignore
            scheme='postgresql+asyncpg',
            user=values.get('TEST_DB_USER'),
            password=values.get('TEST_DB_PASSWORD'),
            host=values.get('TEST_DB_HOST'),
            port=str(values.get('TEST_DB_PORT')),
            path=f'/{values.get("TEST_DB_NAME") or ""}',
        )


settings = Settings()

# logging_config.dictConfig(LOGGING)
