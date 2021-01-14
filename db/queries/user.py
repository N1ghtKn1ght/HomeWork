from api.request import  RequestCreateUserDto
from db.database import DBSession
from db.exceptions import LoginExistsException
from db.models import DBUser


def create_user(session: DBSession, user: RequestCreateUserDto) -> DBUser:
    new_user = DBUser(
        first_name=user.first_name,
        last_name=user.last_name,
        login=user.login,
        password=user.password,
    )
    if session.get_user_by_login(new_user.login) is not None:
        raise LoginExistsException
    session.add_model(new_user)

    return new_user