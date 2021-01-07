from sqlalchemy import Column, VARCHAR, Integer

from db.models.base import BaseModel


class DBUser(BaseModel):

    __tablename__ = 'users'

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    login = Column(
        VARCHAR(50),
        unique=True,
        primary_key=True,
    )
    password = Column(VARCHAR(50))
    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))
