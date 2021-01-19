from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.create_message import RequestCreateMessageDto
from api.response.get_messages import ResponseGetMessagesDtoSchema

from db.database import DBSession
from db.exceptions import DBLoginDoesntExistException, DBDataError, DBIntegrityError
from db.queries import message as message_queries

from helpers.auth.exceptions import ReadTokenException
from helpers.auth.token import read_token

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBLoginNotFound, SanicTokenIsNotReadable, SanicDBException


class MessageEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)

        try:
            login = read_token(request.token, self.config)['login']
        except ReadTokenException as error:
            raise SanicTokenIsNotReadable(str(error))

        try:
            message_queries.create_message(session=session, message=request_model, sender=login)
            session.commit_session()
        except DBLoginDoesntExistException:
            raise SanicDBLoginNotFound('User not found')
        except(DBDataError, DBIntegrityError) as error:
            raise SanicDBException(str(error))

        return await self.make_response_json(body={}, status=201)

    async def method_get(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:

        try:
            login = read_token(request.token, self.config)['login']
        except ReadTokenException as error:
            raise SanicTokenIsNotReadable(str(error))

        db_messages = message_queries.get_message(session=session, login=login)

        response_body = {
            'messages': ResponseGetMessagesDtoSchema(many=True).dump(db_messages)
        }

        return await self.make_response_json(body=response_body, status=200)
