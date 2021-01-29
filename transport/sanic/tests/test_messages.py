import pytest
import datetime

from db.models import DBMessage
from transport.sanic.endpoints import MessagesEndpoint, MessageEndpoint


@pytest.fixture
def token() -> dict:
    return {'id_auth': 1}


@pytest.fixture
def db_message() -> DBMessage:
    message = DBMessage(
        recipient_id=1,
        message="Hi",
        sender_id=1,
    )
    DBMessage.id = 1
    DBMessage.created_at = DBMessage.updated_at = datetime.datetime.utcnow()

    return message


@pytest.mark.asyncio
async def test_get_messages(request_factory, patched_context, mocker):
    patched_query = mocker.patch('db.queries.message.get_message')
    patched_query.return_value = []

    request = request_factory(method='get')
    endpoint = MessagesEndpoint(None, patched_context, '', ())

    response = await endpoint(request=request, token={})

    assert response.status == 200


@pytest.mark.asyncio
async def test_check_false_auth_get_messages(request_factory, patched_context):
    request = request_factory(method='get')
    endpoint = MessagesEndpoint(None, patched_context, '', (), auth_required=True)

    headers = {
        'Authorization': 'no'
    }

    response = await endpoint(request=request, headers=headers)

    assert response.status == 401


@pytest.mark.asyncio
async def test_get_message_by_id(request_factory, patched_context, mocker, token, db_message):
    patched_query = mocker.patch('db.queries.message.get_message')
    patched_query.return_value = db_message

    request = request_factory(method='get')
    endpoint = MessageEndpoint(None, patched_context, '', ())

    response = await endpoint(request=request, token=token, mid=1)

    assert response.status == 200


@pytest.mark.asyncio
async def test_get_message_by_id_code_forbidden(request_factory, patched_context, mocker, token, db_message):
    patched_query = mocker.patch('db.queries.message.get_message')
    patched_query.return_value = db_message

    request = request_factory(method='get')
    endpoint = MessageEndpoint(None, patched_context, '', ())

    token['id_auth'] = 2

    response = await endpoint(request=request, token=token, mid=1)

    assert response.status == 403


@pytest.mark.asyncio
async def test_delete_message(request_factory, patched_context, mocker, token, db_message):
    patched_query = mocker.patch('db.queries.message.get_message')
    patched_query.return_value = db_message
    mocker.patch('db.queries.message.delete_message')
    mocker.patch('db.database.DBSession.commit_session')

    request = request_factory(method='delete')

    endpoint = MessageEndpoint(None, patched_context, '', ())

    response = await endpoint(request=request, token=token, mid=1)

    assert response.status == 204
