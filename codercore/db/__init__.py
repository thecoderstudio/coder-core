from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from codercore.db.models import Base

Session = sessionmaker()


def init_sqlalchemy(connection_url: str) -> Engine:
    engine = create_engine(connection_url)
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    return engine


def get_connection_url(driver: str, user: str, password: str, host: str,
                       database: str) -> str:
    return f"{driver}://{user}:{password}@{host}/{database}"
