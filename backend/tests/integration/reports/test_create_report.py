import pytest
from faker import Faker
from app.models import User


@pytest.fixture(scope="function")
def user(db_session) -> User:
    fake = Faker()
    fake_name = fake.name()
    fake_user_name = fake.user_name()
    # Create User
    user = User(username=fake_user_name, name=fake_name)
    db_session.add(user)
    db_session.commit()
    return user


@pytest.mark.integration
def test_create_report(client, user):
    # Use the client to make a request to create a report
    response = client.post(
        f"/api/reports/{user.id}",
        json={"name": "Test Created Report", "data": "Test created data content"},
    )

    # Check if the response status code is 200 OK
    assert (
        response.status_code == 200
    ), f"Expected 200 OK, got {response.status_code}. Response body: {response.json()}"

    # Check if the response data matches what was added
    response_data = response.json()
    assert response_data["name"] == "Test Created Report", "Report name mismatch"
    assert response_data["data"] == "Test created data content", "Report data mismatch"
    print("Response data:", response_data)
