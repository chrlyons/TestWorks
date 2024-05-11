import pytest


@pytest.mark.integration
def test_create_user(client):
    # Use the client to make a request to create a user
    response = client.post("/api/users/", json={"username": "testuser", "name": "Test User"})

    # Check if the response status code is 200 OK
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response body: {response.json()}"

    # Check if the response data matches what was added
    response_data = response.json()
    assert response_data["username"] == "testuser", "Username mismatch"
    assert response_data["name"] == "Test User", "User name mismatch"
    print("Response data:", response_data)
