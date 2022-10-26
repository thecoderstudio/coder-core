from codercore.db.alembic import get_table_metadata_from_db
from tests.db.models import Sample


def test_get_table_metadata_from_db(db_session):
    sample_table = get_table_metadata_from_db(
        'sample',
        db_session.bind
    )
    assert sample_table.name == Sample.__table__.name
