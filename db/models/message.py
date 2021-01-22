from sqlalchemy import Column, VARCHAR, BOOLEAN

from db.models.base import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'

    message = Column(VARCHAR(255))
    recipient = Column(VARCHAR(50))
    sender = Column(VARCHAR)
    is_delete = Column(BOOLEAN, default=False)
