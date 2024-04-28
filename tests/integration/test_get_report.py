import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.routes.users import get_db
from app.models import Base, User, Report
from dotenv import load_dotenv

from os import getenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    # Explicitly begin a nested transaction
    db_session.begin_nested()

    @event.listens_for(db_session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def user_and_report(db_session) -> [User, Report]:
    # Create User
    user = User(username="testuser", name="Test User")
    db_session.add(user)
    db_session.commit()

    # Create Report associated with the test user
    report = Report(name="Test Report", data="Test data content", user_id=user.id)
    db_session.add(report)
    db_session.commit()
    return [user, report]


def test_get_report(client, user_and_report):
    # Use the client to make a request to the get_report endpoint
    user_data: User = user_and_report[0]
    report_data: Report = user_and_report[1]
    response = client.get(f"/api/reports/{user_data.id}/{report_data.id}")

    # Check if the response status code is 200 OK
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response body: {response.json()}"

    # Check if the response data matches what was added
    response_data = response.json()
    assert response_data["id"] == report_data.id, "Report ID mismatch"
    assert response_data["name"] == "Test Report", "Report name mismatch"
    assert response_data["data"] == "Test data content", "Report data mismatch"
    print("Response data:", response_data)
