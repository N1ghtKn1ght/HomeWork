from api.request.create_message import RequestCreateMessageDto
from db.database import DBSession
from db.exceptions import DBLoginDoesntExistException
from db.models import DBMessage


def create_message(session: DBSession, message: RequestCreateMessageDto, sender: str) -> DBMessage:
    new_message = DBMessage(
        recipient=message.recipient,
        message=message.message,
        sender=sender,
    )
    if session.get_user_by_login(message.recipient) is None:
        raise DBLoginDoesntExistException
    session.add_model(new_message)

    return new_message


def get_message(session: DBSession, login: str):
    return session.get_message_by_login(login=login)
