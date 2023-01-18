import pytest
from fastapi.testclient import TestClient

from db.db import get_session
from main import app
from tests.conftest import override_get_db_session

app.dependency_overrides[get_session] = override_get_db_session

client = TestClient(app)


class TestApiBaseHandle:

    @pytest.mark.asyncio
    async def test_root_handler(self):
        url = app.url_path_for('root_handler')
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == {'version': 'v1'}

    @pytest.mark.asyncio
    async def test_ping_db(self):
        url = app.url_path_for('ping_db')
        response = client.get(url)
        assert response.status_code == 200


class TestApiHistoryHandle:

    # TODO Падает с ошибкой "got Future <Future pending cb=[Protocol._on_waiter_completed()]>
    #  attached to a different loop". Спросить у наставника о вариантах решения проблемы.
    @pytest.mark.asyncio
    async def test_get_status(self, history_items):
        url = app.url_path_for('get_status')
        response = client.get(url)
        assert response.status_code == 200


class TestApiRequestHandle:

    # TODO Падает с ошибкой "got Future <Future pending cb=[Protocol._on_waiter_completed()]>
    #  attached to a different loop". Спросить у наставника о вариантах решения проблемы.
    @pytest.mark.asyncio
    async def test_get_request(self, history_items, url_items):
        url_obj, deleted_url_obj = url_items
        url = app.url_path_for('get_request', url_id=url_obj.id)
        response = client.get(url)
        assert response.status_code == 200


class TestApiUrlHandle:

    # TODO Падает с ошибкой "got Future <Future pending cb=[Protocol._on_waiter_completed()]>
    #  attached to a different loop". Спросить у наставника о вариантах решения проблемы.
    @pytest.mark.asyncio
    async def test_read_urls(self, history_items):
        url = app.url_path_for('read_urls')
        response = client.get(url)
        assert response.status_code == 200
