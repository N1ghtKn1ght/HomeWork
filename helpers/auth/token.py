import datetime

import jwt
import jwt.exceptions

from configs.config import ApplicationConfig
from helpers.auth.exceptions import ReadTokenException


def create_token(payload: dict, config: ApplicationConfig) -> str:
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(weeks=1)
    return jwt.encode(payload, config.jwt.secret, algorithm='HS256')


def read_token(token: str, config: ApplicationConfig) -> dict:
    try:
        return jwt.decode(token, config.jwt.secret, algorithms='HS256')
    except (jwt.PyJWKError, jwt.DecodeError):
        raise ReadTokenException
