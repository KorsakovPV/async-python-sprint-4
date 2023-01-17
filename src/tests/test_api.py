import httpx
import aiohttp
import pytest
# from aioresponses import aioresponses
from fastapi import FastAPI
from fastapi.testclient import TestClient


from db.db import get_session
from main import app
from tests.conftest import override_get_db_session

app.dependency_overrides[get_session] = override_get_db_session


client = TestClient(app)

@pytest.mark.asyncio
async def test_read_main():
    url = app.url_path_for('root_handler')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

class TestApiBaseHandleHttpx:

    # @pytest.mark.anyio
    async def test_root_handler(self):
        url = app.url_path_for('root_handler')
        async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(url)
        assert response.status_code == 200
        assert response.json() == {'version': 'v1'}

    # @pytest.mark.anyio
    async def test_ping_db(self):
        url = app.url_path_for('ping_db')
        async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(url)
        assert response.status_code == 200


# @pytest.mark.anyio
# async def test_root():
#     client = TestClient(app)
#
#     with aioresponses() as mocked:
#         mocked.get("http://httpbin.org/get", status=200, body='{"test": true}')
#
#         response = client.get("/")
#
#         assert response.json() == {"test": True}


# class TestApiBaseHandleAiohttp:
#
#     @pytest.mark.asyncio
#     async def test_get_1(self, aiohttp_client):
#         client = await aiohttp_client(app())
#         resp = await client.get('/user/')
#         assert resp.status == 200
#         resp_json = await resp.json()
#         print(resp_json)

    # @pytest.mark.anyio
    # async def test_root_handler(self):
    #     url = app.url_path_for('root_handler')
    #     async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
    #         response = await ac.get(url)
    #     assert response.status_code == 200
    #     assert response.json() == {'version': 'v1'}

# class TestApiHistoryHandle:
#     @pytest.mark.anyio
#     async def test_get_status(self):
#         url = app.url_path_for('get_status')
#         async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
#             response = await ac.get(url)
#         assert response.status_code == 200
#         assert response.json() == []