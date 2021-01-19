import bcrypt

from helpers.password.exception import GeneratePasswordHashException, CheckPasswordHashException


def generate_hash(password: str) -> bytes:
    try:
        return bcrypt.hashpw(
            password=password.encode(),
            salt=bcrypt.gensalt(),
        )
    except (TypeError, ValueError) as error:
        raise GeneratePasswordHashException(str(error))


def check_hash(password: str, hsh: bytes):
    try:
        result = bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hsh,
        )
    except (TypeError, ValueError) as error:
        raise CheckPasswordHashException(str(error))

    if not result:
        raise CheckPasswordHashException
