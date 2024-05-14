import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from unittest.mock import patch, MagicMock
from app.database import get_db

TEST_DATABASE_URL = "sqlite:///:memory:"

TestEngine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestEngine)

Base = declarative_base()


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=TestEngine)
    yield
    Base.metadata.drop_all(bind=TestEngine)


@pytest.mark.unit
def test_get_db(setup_database):
    with patch("app.database.SessionLocal") as mock_session:
        mock_db = MagicMock()
        mock_session.return_value = mock_db

        with next(get_db()) as db:
            assert isinstance(db, MagicMock)

        mock_db.close.assert_called_once()
