from unittest.mock import patch

from google.cloud.sql.connector import IPTypes
from sqlalchemy.ext.asyncio import AsyncSession

from codercore.db import (
    Session,
    get_connection_url,
    get_connection_with_auto_iam_creator,
    select,
    sessionmaker,
)


def test_get_connection_url():
    connection_url = get_connection_url(
        **{
            "driver": "postgresql",
            "user": "test",
            "password": "test",
            "host": "localhost",
            "database": "test",
        }
    )

    assert connection_url == "postgresql://test:test@localhost/test"


def test_sessionmaker(mocker):
    connection_url = "postgresql://test:test@localhost/test"
    engine = mocker.MagicMock()
    with (
        patch("codercore.db.create_async_engine", return_value=engine) as engine_mock,
        patch("codercore.db.Base") as base_mock,
        patch("codercore.db.sessionmaker_") as sessionmaker_mock,
    ):
        sessionmaker(connection_url)

    engine_mock.assert_called_once_with(connection_url, poolclass=None)
    base_mock.metadata.bind == engine
    sessionmaker_mock.assert_called_once_with(engine, class_=AsyncSession)


def test_sessionmaker_using_creator(mocker):
    connection_url = "postgresql+asyncpg://"
    engine = mocker.MagicMock()
    creator = mocker.MagicMock()
    with (
        patch("codercore.db.create_async_engine", return_value=engine) as engine_mock,
        patch("codercore.db.Base") as base_mock,
        patch("codercore.db.sessionmaker_") as sessionmaker_mock,
    ):
        sessionmaker(connection_url, creator=creator)

    engine_mock.assert_called_once_with(connection_url, poolclass=None, creator=creator)
    base_mock.metadata.bind == engine
    sessionmaker_mock.assert_called_once_with(engine, class_=AsyncSession)


def test_session(mocker):
    session_mock = mocker.MagicMock()
    connection_url = "postgresql://test:test@localhost/test"
    with patch(
        "codercore.db.sessionmaker", return_value=session_mock
    ) as sessionmaker_mock:
        session = Session(connection_url)

    sessionmaker_mock.assert_called_once_with(connection_url)
    assert session == session_mock()


async def test_get_connection_with_auto_iam_creator(mocker):
    instance_connection_name = "connection"
    database = "database"
    user = "user"
    expected_connection = mocker.MagicMock()
    connector = mocker.MagicMock()
    connector.connect_async.return_value = expected_connection
    with (
        patch("codercore.db.create_async_connector", return_value=connector),
        patch("codercore.db.AsyncAdapt_asyncpg_connection") as adapted_connection,
        patch("codercore.db.await_only") as await_only_mock,
    ):
        creator = await get_connection_with_auto_iam_creator(
            instance_connection_name,
            user,
            database,
        )

        connection = creator()
    assert connection == adapted_connection(
        "asyncpg", await_only_mock(expected_connection)
    )
    connector.connect_async.assert_called_once_with(
        instance_connection_name,
        "asyncpg",
        user=user,
        db=database,
        enable_iam_auth=True,
        ip_type=IPTypes.PUBLIC,
    )


def test_select(mocker):
    column_mock = mocker.MagicMock()
    with patch("codercore.db.sa_select") as select_mock:
        statement_mock = select(column_mock)

    assert statement_mock.paginate is not None
    select_mock.assert_called_once_with(column_mock)
