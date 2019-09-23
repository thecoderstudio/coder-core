import datetime
import uuid

from sqlalchemy import Column, DateTime, String

from codercore.db import Base, DBSession as session
from codercore.db.type import UUID


class UserMixin(Base):
    __tablename__ = 'user'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String(500), nullable=False)
    password_hash = Column(String(119), nullable=False)
    password_salt = Column(String(29), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow,
                          nullable=False)


def get_user_by_email(email):
    return session.query(UserMixin).filter(UserMixin.email == email)
