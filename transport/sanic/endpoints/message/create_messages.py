from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.create_message import RequestCreateMessageDto
from api.response.get_messages import ResponseGetMessagesDtoSchema

from db.database import DBSession
from db.exceptions import DBDataError, DBIntegrityError, DBUserNotExistsException
from db.queries import message as message_queries

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicUserNotFound


class MessagesEndpoint(BaseEndpoint):

    async def method_post(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)

        try:
            message_queries.create_message(session=session, message=request_model, sender=token.get('id_auth'))
            session.commit_session()
        except DBUserNotExistsException:
            raise SanicUserNotFound('User not found')
        except(DBDataError, DBIntegrityError) as error:
            raise SanicDBException(str(error))

        return await self.make_response_json(body={}, status=201)

    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        db_messages = message_queries.get_message(session=session, user_id=token.get('id_auth'))

        response_body = {
            'received_messages': ResponseGetMessagesDtoSchema(many=True).dump(db_messages)
        }

        return await self.make_response_json(body=response_body, status=200)
