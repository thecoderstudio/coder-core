from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionEvents

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionEvents()))
Base = declarative_base()
