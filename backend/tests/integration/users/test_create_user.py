import pytest

from faker import Faker

from app.database import get_db
from app.models import User
from app.schema import UserCreate
from app.crud import (
    remove_user_from_database,
    create_user,
)


@pytest.mark.integration
def test_create_user(client):
    fake = Faker()
    fake_name = fake.name()
    fake_user_name = fake.user_name()

    response = client.post(
        "/api/users", json={"name": fake_name, "username": fake_user_name}
    )

    # Check if the response status code is 200 OK
    assert (
        response.status_code == 200
    ), f"Expected 200 OK, got {response.status_code}. Response body: {response.json()}"

    # Check if the response data matches what was added
    response_data = response.json()[0]
    assert response_data["username"] == fake_user_name, "Username mismatch"
    assert response_data["name"] == fake_name, "User name mismatch"
    print("Response data:", response_data)


def test_remove_user_from_database():
    fake = Faker()
    # Create a test user in the database
    unique_username = fake.user_name()
    name = fake.name()
    user_data = UserCreate(username=unique_username, name=name)
    db_user, _ = create_user(user_data)

    # Remove the user using the function being tested
    remove_user_from_database(str(db_user.id))

    # Check if the user is no longer in the database
    db = next(get_db())
    deleted_user = db.query(User).filter(User.id == db_user.id).first()
    assert deleted_user is None
