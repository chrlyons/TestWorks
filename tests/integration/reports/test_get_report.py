import pytest
from backend.models import User, Report


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


@pytest.mark.integration
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


@pytest.mark.integration
def test_get_invalid_report(client):
    # Use the client to make a request to the get_report endpoint
    response = client.get(f"/api/reports/1234567/98765")

    # Check if the response status code is 404 Not Found
    assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}. Response body: {response.json()}"

    # Check if the response data matches error
    response_data = response.json()
    assert response_data["detail"] == "Report not found", "Report found"
    print("Response data:", response_data)

