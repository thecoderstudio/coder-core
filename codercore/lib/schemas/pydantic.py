from pydantic import BaseModel
from pydantic.config import ConfigDict


class FromAttributesBase(BaseModel):
    """Pydantic base model with from_attributes enabled for ORM model conversion."""

    model_config: ConfigDict = {"from_attributes": True}
