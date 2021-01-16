from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateUserDto
from db.database import DBSession
from helpers.password import generate_hash
from transport.sanic.endpoints import BaseEndpoint
from db.exceptions import DBIntegrityError, DBDataError, LoginExistsException

from db.queries import user as user_queries


class UserEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateUserDto(body)

        hashed_password = generate_hash(request_model.password)

        try:
            user_queries.create_user(session=session, user=request_model, hashed_password=hashed_password)
        except LoginExistsException:
            return await self.make_response_json(status=409, message='login exits')
        except(DBDataError, DBIntegrityError) as error:
            return await self.make_response_json(status=500, message=f'My bad: {str(error)}')
        session.commit_session()

        return await self.make_response_json(body={}, status=201)


