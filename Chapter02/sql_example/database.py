from sqlalchemy import create_engine

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase
)

# Connection string for SQLite DB
DATABASE_URL = "sqlite:///./test.db" 

# Represents the core interface to the database
engine = create_engine(DATABASE_URL)

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


# Create tables on DB
Base.metadata.create_all(bind=engine)