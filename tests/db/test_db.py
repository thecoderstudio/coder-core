from unittest.mock import patch

from sqlalchemy.ext.asyncio import AsyncSession

from codercore.db import get_connection_url, sessionmaker, Session


def test_get_connection_url():
    connection_url = get_connection_url(**{
        'driver': 'postgresql',
        'user': 'test',
        'password': 'test',
        'host': 'localhost',
        'database': 'test'
    })

    assert connection_url == "postgresql://test:test@localhost/test"


def test_sessionmaker(mocker):
    connection_url = "postgresql://test:test@localhost/test"
    engine = mocker.MagicMock()
    with (
        patch('codercore.db.create_async_engine',
              return_value=engine) as engine_mock,
        patch('codercore.db.Base') as base_mock,
        patch('codercore.db.sessionmaker_') as sessionmaker_mock
    ):
        sessionmaker(connection_url)

    engine_mock.assert_called_once_with(connection_url)
    base_mock.metadata.bind == engine
    sessionmaker_mock.assert_called_once_with(engine, class_=AsyncSession)


def test_session(mocker):
    session_mock = mocker.MagicMock()
    connection_url = "postgresql://test:test@localhost/test"
    with patch(
        'codercore.db.sessionmaker',
        return_value=session_mock
    ) as sessionmaker_mock:
        session = Session(connection_url)

    sessionmaker_mock.assert_called_once_with(connection_url)
    assert session == session_mock()
