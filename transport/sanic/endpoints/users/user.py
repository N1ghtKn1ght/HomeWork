from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateUserDto
from api.response import ResponseGetUserDto
from transport.sanic.endpoints import BaseEndpoint

from db.queries import user as user_queries


class UserEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateUserDto(body)

        db_user = user_queries.create_user(session=session, user=request_model)
        session.commit_session()

        request_model = ResponseGetUserDto(db_user)

        return await self.make_response_json(body=request_model.dump(), status=201)


