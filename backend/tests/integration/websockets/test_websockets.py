import pytest
from starlette.testclient import TestClient
from unittest.mock import patch
from jose import jwt
from app.main import app


class MockUser:
    id = 1
    username = "test@example.com"


@pytest.mark.asyncio
@pytest.mark.integration
def test_websocket_endpoint_accepts_valid_token():
    client = TestClient(app)
    valid_token = jwt.encode({"sub": "test@example.com"}, "secret", algorithm="HS256")

    with patch("jose.jwt.decode", return_value={"sub": "test@example.com"}):
        with patch("app.crud.get_user_by_username", return_value=MockUser()):
            with patch("redis.Redis.ttl", return_value=3600):
                with client.websocket_connect(
                    f"/api/ws/test@example.com?token={valid_token}"
                ) as websocket:
                    data = websocket.receive_json()
                    expected_time = 3600
                    actual_time = int(data["message"].split(": ")[1].split(" ")[0])
                    assert (
                        abs(actual_time - expected_time) <= 10
                    ), "Session time is not within the expected range"
