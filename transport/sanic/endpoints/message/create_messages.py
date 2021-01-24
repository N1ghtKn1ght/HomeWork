from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.create_message import RequestCreateMessageDto
from api.response.get_messages import ResponseGetMessagesDtoSchema

from db.database import DBSession
from db.exceptions import DBLoginDoesntExistException, DBDataError, DBIntegrityError
from db.queries import message as message_queries
from db.queries import user as user_queries

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBLoginNotFound, SanicDBException


class MessagesEndpoint(BaseEndpoint):

    async def method_post(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)

        db_user = user_queries.get_user(session=session, user_id=token.get('id_auth'))

        try:
            message_queries.create_message(session=session, message=request_model, sender=db_user.login)
            session.commit_session()
        except DBLoginDoesntExistException:
            raise SanicDBLoginNotFound('User not found')
        except(DBDataError, DBIntegrityError) as error:
            raise SanicDBException(str(error))

        return await self.make_response_json(body={}, status=201)

    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        db_user = user_queries.get_user(session=session, user_id=token.get('id_auth'))

        db_messages = message_queries.get_message(session=session, login=db_user.login)

        response_body = {
            'received_messages': ResponseGetMessagesDtoSchema(many=True).dump(db_messages)
        }

        return await self.make_response_json(body=response_body, status=200)
