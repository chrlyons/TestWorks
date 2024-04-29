import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.models import Base, User, Report


@pytest.fixture(scope="module")
def engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture(scope="function")
def session(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    Base.metadata.drop_all(engine)


@pytest.mark.unit
@pytest.mark.model
def test_user_creation(session):
    user = User(username='johndoe', name='John Doe')
    session.add(user)
    session.commit()
    assert user.id is not None


@pytest.mark.unit
@pytest.mark.model
def test_username_uniqueness(session):
    user1 = User(username='janedoe', name='Jane Doe')
    session.add(user1)
    session.commit()
    user2 = User(username='janedoe', name='Jane Smith')
    session.add(user2)
    with pytest.raises(IntegrityError):
        session.commit()


@pytest.mark.unit
@pytest.mark.model
def test_user_report_relationship(session):
    user = User(username='newuser', name='New User')
    report = Report(name='Report 1', data='Some data', owner=user)
    session.add(user)
    session.add(report)
    session.commit()
    assert report.user_id == user.id
    assert user.reports[0].id == report.id
