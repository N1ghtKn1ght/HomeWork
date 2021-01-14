from sqlalchemy import Column, VARCHAR, VARBINARY

from db.models.base import BaseModel


class DBUser(BaseModel):

    __tablename__ = 'users'

    login = Column(
        VARCHAR(50),
        unique=True,
        nullable=False,
    )
    password = Column(
        VARBINARY,
        nullable=False
    )
    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))
