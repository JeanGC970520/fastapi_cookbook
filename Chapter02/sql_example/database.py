from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase
)


class Base(DeclarativeBase):
    """
        Class to mantains a catalog of classes and tables
    """
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str]
    email: Mapped[str]
