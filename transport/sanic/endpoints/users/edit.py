from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.patch_user import RequestPatchUserDto
from api.response.patch_user import ResponsePatchUserDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException, DBDataError, DBIntegrityError
from transport.sanic.endpoints import BaseEndpoint

from db.queries import user as user_queries
from transport.sanic.exceptions import SanicUserNotFound, SanicDBException


class EditUserEndpoint(BaseEndpoint):
    async def method_patch(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        request_model = RequestPatchUserDto(body)

        try:
            user = user_queries.patch_user(session, request_model, token['id_auth'])
        except DBUserNotExistsException:
            raise SanicUserNotFound('User not found')

        try:
            session.commit_session()
        except(DBDataError, DBIntegrityError) as error:
            raise SanicDBException(str(error))

        response_model = ResponsePatchUserDto(user)

        return await self.make_response_json(status=200, body=response_model.dump())
