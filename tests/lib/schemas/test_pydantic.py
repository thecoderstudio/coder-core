from codercore.lib.schemas.pydantic import ORMBase


def test_orm_base():
    assert ORMBase.Config.orm_mode
