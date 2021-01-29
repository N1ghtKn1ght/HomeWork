import datetime

import jwt
import jwt.exceptions

from helpers.auth.config import jwtConfig
from helpers.auth.exceptions import ReadTokenException


def create_token(data: dict, *, lifetime: int = 1) -> str:
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=lifetime)
    }
    payload.update(data)
    return jwt.encode(payload, jwtConfig.secret, algorithm='HS256')


def read_token(token: str) -> dict:
    try:
        return jwt.decode(token, jwtConfig.secret, algorithms='HS256')
    except (jwt.PyJWKError, jwt.DecodeError):
        raise ReadTokenException
