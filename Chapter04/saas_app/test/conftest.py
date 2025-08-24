"""Module to defines testing configurations
with pytest, all fixtures creates here will be
access from all test under the project's root
folder.
"""

import pytest
from passlib.context import CryptContext
from sqlalchemy import QueuePool, create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=QueuePool,
    )

    session_local = sessionmaker(engine)

    db_session = session_local()

    Base.metadata.create_all(bind=engine)

    yield db_session

    Base.metadata.drop_all(bind=engine)

    db_session.close()
