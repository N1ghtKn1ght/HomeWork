from api.request import RequestCreateUserDto
from db.database import DBSession
from db.exceptions import DBLoginExistsException
from db.models import DBUser


def create_user(session: DBSession, user: RequestCreateUserDto, hashed_password: bytes) -> DBUser:
    new_user = DBUser(
        first_name=user.first_name,
        last_name=user.last_name,
        login=user.login,
        password=hashed_password,
    )
    if session.get_user_by_login(new_user.login) is not None:
        raise DBLoginExistsException
    session.add_model(new_user)

    return new_user


def get_user(session: DBSession, login: str):
    return session.get_user_by_login(login)