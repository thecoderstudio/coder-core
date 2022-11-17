import os

from pytest import fixture

from codercore.test.fixtures import (
    connection_settings as connection_settings_,
    sync_db_connection_url as sync_db_connection_url_,
    async_db_connection_url as async_db_connection_url_,
    db_session as db_session_,
    DBSession as DBSession_,
    redis_connection as redis_connection_,
    clean_up_for_worker as clean_up_for_worker_,
)

sync_db_connection_url = fixture(sync_db_connection_url_, scope="session")
async_db_connection_url = fixture(async_db_connection_url_, scope="session")
DBSession = fixture(DBSession_)
db_session = fixture(db_session_)
redis_connection = fixture(redis_connection_)
clean_up_for_worker = fixture(clean_up_for_worker_, scope="session", autouse=True)


@fixture(scope="session")
def connection_settings(worker_id: str) -> dict[str, str]:
    return connection_settings_(
        os.environ["POSTGRES_USER"],
        os.environ["POSTGRES_PASSWORD"],
        os.environ["POSTGRES_HOST"],
        worker_id,
    )
