from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.auth_user import RequestAuthUserDto
from db.database import DBSession
from transport.sanic.endpoints import BaseEndpoint
from db.queries import user as user_queries
from db.exceptions import DBLoginDoesntExistException
from transport.sanic.exceptions import SanicDBLoginNotFound, SanicPasswordHashException
from helpers.password.to_hash import check_hash
from helpers.password.exception import CheckPasswordHashException
from helpers.auth.token import create_token


class AuthUserEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:
        request_model = RequestAuthUserDto(body)

        try:
            db_user = user_queries.get_user(session=session, login=request_model.login)
            check_hash(request_model.password, db_user.password)
        except DBLoginDoesntExistException:
            raise SanicDBLoginNotFound('Login not found')
        except CheckPasswordHashException:
            raise SanicPasswordHashException("password is wrong")

        payload = {
            'login': db_user.login,
        }

        token = create_token(payload, self.config)

        response_body = {
            'Authorization': token
        }

        return await self.make_response_json(body=response_body, status=200,)


