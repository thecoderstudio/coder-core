from sqlalchemy import Column, Integer, String

from codercore.db.models import Base


class Sample(Base):
    __tablename__ = "sample"
    value = Column(String, primary_key=True)
    count = Column(Integer, default=0)
