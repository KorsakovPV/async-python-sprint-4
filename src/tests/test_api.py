import httpx
import pytest

from db.db import get_session
from main import app
from tests.conftest import override_get_db_session

app.dependency_overrides[get_session] = override_get_db_session

class TestApiBaseHandle:

    @pytest.mark.anyio
    async def test_root_handler(self):
        url = app.url_path_for('root_handler')
        async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(url)
        assert response.status_code == 200
        assert response.json() == {'version': 'v1'}

    @pytest.mark.anyio
    async def test_ping_db(self):
        url = app.url_path_for('ping_db')
        async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(url)
        assert response.status_code == 200


class TestApiHistoryHandle:
    @pytest.mark.anyio
    async def test_get_status(self):
        url = app.url_path_for('get_status')
        async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(url)
        assert response.status_code == 200
        assert response.json() == []