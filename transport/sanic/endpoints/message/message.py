from urllib.request import Request

from sanic.response import BaseHTTPResponse

from api.response.get_messages import ResponseGetMessagesDto
from db.database import DBSession
from db.exceptions import DBMessageDoesntExistException
from transport.sanic.endpoints import BaseEndpoint
from db.queries import message as message_queries
from transport.sanic.exceptions import SanicMessageNotFound


class MessageEndpoint(BaseEndpoint):
    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict,  mid: int,  *args, **kwargs
    ) -> BaseHTTPResponse:
        try:
            db_message = message_queries.get_message(session=session, mid=mid)
        except DBMessageDoesntExistException:
            raise SanicMessageNotFound('message not found')

        response_model = ResponseGetMessagesDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=200)
