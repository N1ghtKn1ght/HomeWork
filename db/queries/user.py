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


def patch_user(session: DBSession, user: RequestPatchUserDto, uid: int, *, hashed_password: bytes = None) -> DBUser:
    db_user = session.get_user_by_id(uid)

    if hasattr(user, 'login'):
        _change_login(session, user.login, db_user.login)

    for attr in user.fields:
        if hashed_password is not None and attr == 'password':
            setattr(db_user, attr, hashed_password)
        elif hasattr(user, attr):
            setattr(db_user, attr, getattr(user, attr))

    return db_user


def _change_login(session: DBSession, login: str, last_login: str):
    if session.get_user_by_login(login) is not None:
        raise DBLoginExistsException
    db_messages = session.get_messages_for_change_login(last_login)
    for message in db_messages:
        if message.sender == last_login:
            message.sender = login
        if message.recipient == last_login:
            message.recipient = login
    print(db_messages)
    session.commit_session()
