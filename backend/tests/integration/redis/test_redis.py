import pytest
import time
import json

from app.crud import get_user_by_username, redis_client, update_redis_user_session


@pytest.mark.integration
class TestRedisOperations:
    def test_redis_stores_session_on_login(self, client, faker):
        email = faker.email()
        login_data = {"username": email, "password": "secure_password"}
        client.post("/api/login/", data=login_data)
        time.sleep(1)
        user = get_user_by_username(email)
        session_data = redis_client.get(str(user.id)).decode("utf-8")
        redis_client.close()
        assert session_data is not None

    def test_update_redis_user_session(self):
        # Create a test session info
        session_info = {"key": "value"}

        # Update the user's session information in Redis using the function being tested
        user_id = "test_user_id"
        update_redis_user_session(user_id, session_info)

        # Get the updated session information from Redis
        updated_session = redis_client.get(f"user_session:{user_id}")

        # Check if the session information has been updated in Redis
        assert updated_session is not None
        assert json.loads(updated_session) == session_info
