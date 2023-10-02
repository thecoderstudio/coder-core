from codercore.lib.schemas.pydantic import FromAttributesBase


def test_from_attributes_base():
    assert FromAttributesBase.model_config["from_attributes"]
