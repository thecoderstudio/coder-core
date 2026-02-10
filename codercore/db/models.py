from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    """Declarative base for all SQLAlchemy ORM models."""

    def set_fields(self, **kwargs) -> None:
        """Set multiple model attributes from keyword arguments."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __hash__(self) -> int:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return hash(self) == hash(other)
