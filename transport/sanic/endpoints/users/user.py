from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response.get_user import ResponseGetUserDto
from db.database import DBSession
from transport.sanic.endpoints import BaseEndpoint
from db.exceptions import DBUserNotExistsException

from db.queries import user as user_queries
from transport.sanic.exceptions import SanicUserNotExists


class UserEndpoint(BaseEndpoint):
    async def method_get(
            self, request: Request, body: dict, session: DBSession, uid: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            db_user = user_queries.get_user(session=session, user_id=uid)
        except DBUserNotExistsException:
            raise SanicUserNotExists('User is not found')
        response = ResponseGetUserDto(db_user)

        return await self.make_response_json(body=response.dump(), status=200)



