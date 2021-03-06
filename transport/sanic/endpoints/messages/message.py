from urllib.request import Request

from sanic.response import BaseHTTPResponse

from api.request.patch_message import RequestPatchMessageDto
from api.response.get_messages import ResponseGetMessagesDto
from api.response.patch_message import ResponsePatchMessageDto
from db.database import DBSession
from db.exceptions import DBMessageDoesntExistException, DBDataError, DBIntegrityError
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicMessageNotFound, SanicDBException


class MessageEndpoint(BaseEndpoint):
    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict,  mid: int,  *args, **kwargs
    ) -> BaseHTTPResponse:
        try:
            db_message = message_queries.get_message(session=session, mid=mid)
        except DBMessageDoesntExistException:
            raise SanicMessageNotFound('message not found')

        if db_message.recipient_id == token.get('id_auth') or db_message.sender_id == token.get('id_auth'):
            response_model = ResponseGetMessagesDto(db_message)
        else:
            return await self.make_response_json(status=403)

        return await self.make_response_json(body=response_model.dump(), status=200)

    async def method_patch(
            self, request: Request, body: dict, session: DBSession, token: dict,  mid: int, *args, **kwargs
    ) -> BaseHTTPResponse:
        try:
            db_message = message_queries.get_message(session=session, mid=mid)
        except DBMessageDoesntExistException:
            raise SanicMessageNotFound('message not found')

        if db_message.sender_id != token.get('id_auth'):
            return await self.make_response_json(status=403)

        request_model = RequestPatchMessageDto(body)

        message = message_queries.patch_message(db_message, request_model)

        try:
            session.commit_session()
        except(DBDataError, DBIntegrityError) as error:
            raise SanicDBException(str(error))

        response_model = ResponsePatchMessageDto(message)

        return await self.make_response_json(body=response_model.dump())

    async def method_delete(
            self, request: Request, body: dict, session: DBSession, token: dict,  mid: int,  *args, **kwargs
    ) -> BaseHTTPResponse:
        try:
            db_message = message_queries.get_message(session=session, mid=mid)
        except DBMessageDoesntExistException:
            raise SanicMessageNotFound('message not found')

        if db_message.sender_id != token.get('id_auth'):
            return await self.make_response_json(status=403)

        message_queries.delete_message(db_message)

        try:
            session.commit_session()
        except(DBDataError, DBIntegrityError) as error:
            raise SanicDBException(str(error))

        return await self.make_response_json(status=204, body=None)
