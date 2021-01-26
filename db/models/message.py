from sqlalchemy import Column, VARCHAR, BOOLEAN, Integer

from db.models.base import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'

    message = Column(VARCHAR(255))
    recipient_id = Column(Integer)
    sender_id = Column(Integer)
    is_delete = Column(BOOLEAN, default=False)
