
import pytest
from faker import Faker


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
