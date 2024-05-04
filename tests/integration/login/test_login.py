import pytest
from backend.schema import UserCreate
from backend.crud import create_user, create_access_token


@pytest.mark.integration
class TestLogin:
    def test_login_successful(self, client):
        # Test data
        login_data = {"username": "test@example.com", "password": "secure_password"}

        # Make a request to login
        response = client.post("/login/", data=login_data)

        # Assert the response status code is 200 (OK)
        assert response.status_code == 200

        # Assert the response contains the access token and token type
        assert "access_token" in response.json()
        assert "token_type" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_invalid_password(self, client):
        # Test data with invalid password (using "password" which is disallowed)
        login_data = {"username": "test@example.com", "password": "password"}

        # Make a request to login with invalid password
        response = client.post("/login/", data=login_data)

        # Assert the response status code is 400 (Bad Request)
        assert response.status_code == 400

        # Assert the response contains the detail message for invalid password
        assert "Password cannot be 'password'" in response.text

    def test_login_invalid_email(self, client):
        # Test data with invalid email format
        login_data = {"username": "invalidemail", "password": "secure_password"}

        # Make a request to login with invalid email format
        response = client.post("/login/", data=login_data)

        # Assert the response status code is 400 (Bad Request)
        assert response.status_code == 400

        # Assert the response contains the detail message for invalid email
        assert "Invalid email address" in response.text
