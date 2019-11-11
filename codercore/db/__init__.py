import copy
import logging
import transaction

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register

log = logging.getLogger(__name__)

DBSession = scoped_session(sessionmaker())
register(DBSession)
Base = declarative_base()


def commit():
    log.debug("Committing session: %r", DBSession.dirty)
    transaction.commit()


def persist(obj):
    log.debug("persisting object %r", obj)
    DBSession.add(obj)
    DBSession.flush()
    return obj


def rollback():
    log.debug("Rolling back session: %r", DBSession.dirty)
    return DBSession.rollback()


def delete(obj):
    log.debug("deleting object %r", obj)
    DBSession.delete(obj)


def save(obj):
    try:
        obj = persist(obj)
        try:
            id_ = obj.id
        except AttributeError:
            id_ = None
        # Shallow copy to be able to return generated data without having
        # to request the object again to get it in session.
        obj_copy = copy.copy(obj)
    except Exception as e:
        log.critical(
            'Something went wrong saving the {}'.format(
                obj.__class__.__name__),
            exc_info=True)
        rollback()
        raise e
    finally:
        commit()

    return obj_copy, id_
