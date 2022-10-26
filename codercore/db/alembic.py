from typing import Optional

from alembic import op
from sqlalchemy import MetaData
from sqlalchemy.engine import Connectable
from sqlalchemy.sql.schema import Table


def get_table_metadata_from_db(
    table_name: str,
    bind: Optional[Connectable] = None
) -> Table:
    bind = bind if bind else op.get_bind()
    metadata = MetaData()
    metadata.reflect(bind)
    return metadata.tables[table_name]
