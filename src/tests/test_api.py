from unittest import mock

import httpx
import pytest

from main import app
from tests.conftest import async_session_test

# @pytest.mark.asyncio
# async def test_some_asyncio_code():
#     # res = await library.do_something()
#     assert True

class TestApiBaseHandle:

    @pytest.mark.asyncio
    async def test_get_root_handler(self, httpx_mock):
        httpx_mock.add_response()
        url = app.url_path_for('root_handler')

        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(url)
            print(response.status_code)
            print(response.body)
        # assert response.status_code == 200
        # assert response.json() == {"message": "Tomato"}

    @pytest.mark.asyncio
    async def test_get_root_handler1(self, httpx_mock):
        httpx_mock.add_response()
        url = app.url_path_for('ping_db')

        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.patch(url)
            print(response.status_code)
            print(response.body)
        # assert response.status_code == 200
        # assert response.json() == {"message": "Tomato"}




    #
    # async def test_get_2(self):
    #     pass
    # #     client = await aiohttp_client(app())
    # #     resp = await client.get(f'/user/{str(user.id)}')
    # #     assert resp.status == 200
    # #     resp_json = await resp.json()
    # #     assert str(user.id) == resp_json[0].get('id')
    # #     assert user.name == resp_json[0].get('name')
    # #
    # async def test_post(self):
    #     pass
    #     client = await aiohttp_client(app())
    #     resp = await client.post('/user/', json=user_json)
    #     assert resp.status == 201


# class TestApiChatRoomHandle:
#
#     async def test_get_1(self, aiohttp_client, chat_room):
#         client = await aiohttp_client(app())
#         resp = await client.get('/chat_room/')
#         assert resp.status == 200
#         resp_json = await resp.json()
#         assert str(chat_room.id) == resp_json[0].get('id')
#         assert chat_room.name == resp_json[0].get('name')
#
#     async def test_get_2(self, aiohttp_client, chat_room):
#         client = await aiohttp_client(app())
#         resp = await client.get(f'/chat_room/{str(chat_room.id)}')
#         assert resp.status == 200
#         resp_json = await resp.json()
#         assert str(chat_room.id) == resp_json[0].get('id')
#         assert chat_room.name == resp_json[0].get('name')
#
#     async def test_post(self, aiohttp_client, chat_room_json):
#         client = await aiohttp_client(app())
#         resp = await client.post('/chat_room/', json=chat_room_json)
#         assert resp.status == 201
#
#
# class TestApiConnectHandle:
#
#     async def test_get(self, aiohttp_client, connect_chat):
#         client = await aiohttp_client(app())
#         resp = await client.get(f'/connect/{connect_chat.user_id}')
#         assert resp.status == 200
#         resp_json = await resp.json()
#         assert str(connect_chat.chat_room_id) == resp_json[0].get('chat_room_id')
#         assert str(connect_chat.user_id) == resp_json[0].get('user_id')
#
#     async def test_post(self, aiohttp_client, chat_room_json):
#         client = await aiohttp_client(app())
#         resp = await client.post('/connect/', json=chat_room_json)
#         assert resp.status == 201
#
#
# class TestApiMessageHandle:
#     @mock.patch('server.async_session', mock.MagicMock(return_value=async_session_test()))
#     async def test_get(self, aiohttp_client, connect_chat, message):
#         client = await aiohttp_client(app())
#         resp = await client.get(
#             '/message/', json={
#                 'author_id': str(connect_chat.user_id),
#                 'chat_room_id': str(connect_chat.chat_room_id)
#             }
#         )
#         assert resp.status == 200
#         resp_json = await resp.json()
#         print(resp_json)
#         assert str(connect_chat.chat_room_id) == resp_json[0].get('chat_room_id')
#         assert str(connect_chat.user_id) == resp_json[0].get('author_id')
#         assert str(message.message) == resp_json[0].get('message')
#
#     @mock.patch('server.async_session', mock.MagicMock(return_value=async_session_test()))
#     async def test_post(self, aiohttp_client, connect_chat, message_json):
#         client = await aiohttp_client(app())
#         resp = await client.post('/message/', json=message_json)
#         assert resp.status == 201
