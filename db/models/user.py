from sqlalchemy import Column, VARCHAR, Integer, Sequence

from db.models.base import BaseModel


class DBUser(BaseModel):

    __tablename__ = 'users'

    login = Column(
        VARCHAR(50),
        unique=True,
        nullable=False,
    )
    password = Column(VARCHAR(50))
    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))
