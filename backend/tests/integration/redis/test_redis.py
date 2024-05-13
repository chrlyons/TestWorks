import pytest
import time
import json
from unittest.mock import patch
from datetime import datetime, timezone, timedelta

from app.crud import check_user_token_expiration, get_user_by_username, redis_client, update_redis_user_session


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

    @pytest.fixture
    def redis_data(self):
        return {
            "user:1": json.dumps(
                {
                    "token_expires": (
                            datetime.now(timezone.utc) - timedelta(days=1)
                    ).isoformat()
                }
            ),
            "user:2": json.dumps(
                {
                    "token_expires": (
                            datetime.now(timezone.utc) + timedelta(days=1)
                    ).isoformat()
                }
            ),
        }

    def test_check_user_token_expiration(self, redis_data):
        with patch("app.crud.redis_client.scan_iter", return_value=redis_data.keys()):
            with patch(
                    "app.crud.redis_client.get",
                    side_effect=lambda k: redis_data[k].encode("utf-8"),
            ):
                with patch("app.crud.redis_client.ttl", return_value=3600):
                    with patch("app.crud.remove_user_from_database") as mock_remove:
                        check_user_token_expiration()
                        # Assert that remove_user_from_database is called with each user key
                        mock_remove.assert_any_call("user:1")
                        mock_remove.assert_any_call("user:2")
                        # Assert that remove_user_from_database is called exactly twice
                        assert mock_remove.call_count == 2
