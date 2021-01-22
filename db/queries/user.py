from api.request import RequestCreateUserDto
from api.request.patch_user import RequestPatchUserDto
from db.database import DBSession
from db.exceptions import DBLoginExistsException, DBUserNotExistsException
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


def get_user(session: DBSession, *, login: str = None, user_id: int = None) -> DBUser:
    db_user = None
    if login is not None:
        db_user = session.get_user_by_login(login)
    else:
        db_user = session.get_user_by_id(user_id)

    if db_user is None:
        raise DBUserNotExistsException

    return db_user


def patch_user(session: DBSession, user: RequestPatchUserDto, udi: int) -> DBUser:

    db_user = session.get_user_by_id(udi)

    for attr in user.fields:
        if hasattr(user, attr):
            setattr(db_user, attr, getattr(user, attr))

    return db_user
