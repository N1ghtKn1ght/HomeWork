from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateUserDto
from db.database import DBSession
from transport.sanic.endpoints import BaseEndpoint
from db.exceptions import DBIntegrityError, DBDataError, DBLoginExistsException

from db.queries import user as user_queries
from transport.sanic.exceptions import SanicPasswordHashException, SanicLoginExistsException, SanicDBException

from helpers.password import generate_hash
from helpers.password.exception import GeneratePasswordHashException


class CreateUserEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateUserDto(body)

        try:
            hashed_password = generate_hash(request_model.password)
            user_queries.create_user(session=session, user=request_model, hashed_password=hashed_password)
            session.commit_session()
        except GeneratePasswordHashException as error:
            raise SanicPasswordHashException(str(error))
        except DBLoginExistsException:
            raise SanicLoginExistsException('login exits')
        except(DBDataError, DBIntegrityError) as error:
            raise SanicDBException(str(error))

        return await self.make_response_json(status=201)


