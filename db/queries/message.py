from api.request.create_message import RequestCreateMessageDto
from api.request.patch_message import RequestPatchMessageDto
from db.database import DBSession
from db.exceptions import DBLoginDoesntExistException, DBMessageDoesntExistException
from db.models import DBMessage


def create_message(session: DBSession, message: RequestCreateMessageDto, sender: int) -> DBMessage:
    new_message = DBMessage(
        recipient_id=message.recipient_id,
        message=message.message,
        sender_id=sender,
    )
    if session.get_user_by_id(uid=message.recipient_id) is None:
        raise DBLoginDoesntExistException
    session.add_model(new_message)

    return new_message


def get_message(session: DBSession, *, user_id: int = None, mid: int = None) -> DBMessage:
    db_message = None

    if user_id is not None:
        db_message = session.get_messages_by_login(user_id)
    else:
        db_message = session.get_message_by_id(mid)

    if db_message is None:
        raise DBMessageDoesntExistException

    return db_message


def patch_message(db_message: DBMessage, message: RequestPatchMessageDto) -> DBMessage:
    for attr in message.fields:
        if hasattr(message, attr):
            setattr(db_message, attr, getattr(message, attr))

    return db_message


def delete_message(db_message: DBMessage) -> DBMessage:
    db_message.is_delete = True
    return db_message