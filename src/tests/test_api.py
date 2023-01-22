import pytest
from fastapi.testclient import TestClient
from httpx import URL
from fastapi import HTTPException

from main import app
from services.history_service import history_crud
from services.request_service import request_crud
from services.url_service import url_crud

# app.dependency_overrides[get_session] = override_get_db_session

client = TestClient(app)


class TestApiBaseHandle:

    async def test_root_handler(self):
        url = app.url_path_for('root_handler')
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == {'version': 'v1'}

    # TODO Падает с ошибкой "got Future <Future pending cb=[Protocol._on_waiter_completed()]>
    #  attached to a different loop". Спросить у наставника о вариантах решения проблемы.
    # async def test_ping_db(self):
    #     url = app.url_path_for('ping_db')
    #     response = client.get(url)
    #     assert response.status_code == 200


class TestBlockedHostMiddleware:

    async def test_call_available(self):
        url = app.url_path_for('root_handler')
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == {'version': 'v1'}

    async def test_call_blocked0(self):
        url = app.url_path_for('root_handler')
        client.base_url = URL('http://example.com')
        response = client.get(url)
        assert response.status_code == 400
        assert response.text == 'Invalid host header'

    async def test_call_blocked1(self):
        url = app.url_path_for('root_handler')
        client.base_url = URL('http://testserver.example.com')
        response = client.get(url)
        assert response.status_code == 400
        assert response.text == 'Invalid host header'


class TestApiHistoryHandle:

    # TODO Падает с ошибкой "got Future <Future pending cb=[Protocol._on_waiter_completed()]>
    #  attached to a different loop". Спросить у наставника о вариантах решения проблемы.
    # async def test_get_status_with_client(self, history_items):
    #     url = app.url_path_for('get_status')
    #     response = client.get(url)
    #     assert response.status_code == 200

    async def test_get_status(self, history_items, session):
        response = await history_crud.get_multi(
            url_id=None,
            user_id=None,
            domen=None,
            method=None,
            db=session,
            skip=0,
            limit=100
        )
        assert len(response) == 1
        assert response[0].id == history_items.id
        assert response[0].url_id == history_items.url_id
        assert response[0].method == history_items.method


class TestApiRequestHandle:

    # TODO Падает с ошибкой "got Future <Future pending cb=[Protocol._on_waiter_completed()]>
    #  attached to a different loop". Спросить у наставника о вариантах решения проблемы.
    # async def test_get_request_with_client(self, history_items, url_items):
    #     url_obj, deleted_url_obj = url_items
    #     url = app.url_path_for('get_request', url_id=url_obj.id)
    #     response = client.get(url)
    #     assert response.status_code == 200

    async def test_get_request_case0(self, url_items, session):
        url_obj, deleted_url_obj = url_items
        url = await request_crud.custom_request(
            url_id=url_obj.id,
            user_id=None,
            db=session,
            method='GET',
            host='http://testserver'
        )
        assert url == url_obj.url

    async def test_get_request_case1(self, url_items, session):
        url_obj, deleted_url_obj = url_items
        with pytest.raises(HTTPException):
            await request_crud.custom_request(
                url_id=deleted_url_obj.id,
                user_id=None,
                db=session,
                method='GET',
                host='http://testserver'
            )


class TestApiUrlHandle:

    # TODO Падает с ошибкой "got Future <Future pending cb=[Protocol._on_waiter_completed()]>
    #  attached to a different loop". Спросить у наставника о вариантах решения проблемы.
    # async def test_read_urls_with_client(self, history_items):
    #     url = app.url_path_for('read_urls')
    #     response = client.get(url)
    #     assert response.status_code == 200

    async def test_read_urls(self, url_items, session):
        url_obj, _ = url_items
        response = await url_crud.get_multi(db=session, skip=0, limit=100)
        assert isinstance(response, list)
        assert len(response) == 1
        assert url_obj.id == response[0].id
        assert url_obj.url == response[0].url

    async def test_read_url(self, url_items, session):
        url_obj, _ = url_items
        response = await url_crud.get(db=session, id=url_obj.id)
        assert url_obj.id == response.id
        assert url_obj.url == response.url

    async def test_read_url_is_delete(self, url_items, session):
        _, deleted_url_obj = url_items
        response = await url_crud.get(db=session, id=deleted_url_obj.id)
        assert response is None

    async def test_create_url(self, session, new_test_url):
        response = await url_crud.create(db=session, obj_in=new_test_url)
        assert response.url == new_test_url.url

    async def test_update_url(self, url_items, session, new_test_url):
        url_obj, _ = url_items
        response = await url_crud.update(
            db=session,
            id=url_obj.id,
            obj_in=new_test_url
        )
        assert response.url == new_test_url.url

    async def test_delete_url(self, url_items, session):
        url_obj, _ = url_items
        response = await url_crud.delete(
            db=session,
            id=url_obj.id,
        )
        assert response.is_delete is True
